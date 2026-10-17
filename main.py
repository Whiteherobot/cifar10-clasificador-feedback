"""API del clasificador CIFAR-10: predicción, feedback y re-entrenamiento.

uvicorn main:app --reload   (necesita un modelo en models/, ver el cuaderno 02)
"""

import asyncio
import glob
import os
import time
from io import BytesIO

import numpy as np
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from PIL import Image, UnidentifiedImageError

CIFAR_LABELS = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
MAX_BYTES = 5 * 1024 * 1024
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


def preprocess_image(img_bytes: bytes) -> np.ndarray:
    """Bytes de una imagen -> tensor normalizado (1, 32, 32, 3)."""
    if len(img_bytes) > MAX_BYTES:
        raise HTTPException(413, "La imagen supera los 5 MB.")
    try:
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(400, "El archivo no es una imagen válida.") from exc
    if img.size != (32, 32):
        img = img.resize((32, 32), Image.LANCZOS)
    return (np.asarray(img, dtype="float32") / 255.0).reshape(1, 32, 32, 3)


class Clasificador:
    """Modelo actual, feedback guardado y re-entrenamiento.

    El re-entrenamiento se hace sobre una copia del modelo en otro hilo; las
    predicciones siguen con el modelo anterior hasta que la copia termina y se
    reemplaza.
    """

    def __init__(self, models_dir="models", feedback_dir=os.path.join("data", "feedback"), replay_dir="focus"):
        self.models_dir = models_dir
        self.feedback_dir = feedback_dir
        self.replay_dir = replay_dir
        self.modelo = None
        self.ruta_modelo = None
        self._reentrenando = asyncio.Lock()

    # -- modelo ---------------------------------------------------------------
    def ruta_ultimo_modelo(self) -> str:
        """El indicado en models/latest_model.txt o, si no, el .keras más nuevo."""
        latest = os.path.join(self.models_dir, "latest_model.txt")
        if os.path.exists(latest):
            with open(latest, encoding="utf-8") as f:
                candidato = f.read().strip()
            if candidato and os.path.exists(candidato):
                return candidato
        archivos = glob.glob(os.path.join(self.models_dir, "*.keras"))
        if not archivos:
            raise HTTPException(503, "No hay ningún modelo en models/. Entrene uno con el cuaderno 02.")
        return max(archivos, key=os.path.getmtime)

    def cargar(self):
        from tensorflow import keras

        self.ruta_modelo = self.ruta_ultimo_modelo()
        self.modelo = keras.models.load_model(self.ruta_modelo)

    def usar(self, modelo, ruta="(en memoria)"):
        self.modelo, self.ruta_modelo = modelo, ruta

    def predecir(self, img_bytes: bytes):
        if self.modelo is None:
            self.cargar()
        probs = self.modelo.predict(preprocess_image(img_bytes), verbose=0)[0]
        top3 = [(CIFAR_LABELS[i], float(probs[i])) for i in np.argsort(probs)[-3:][::-1]]
        return top3[0][0], top3[0][1], top3

    # -- feedback ---------------------------------------------------------------
    def guardar_feedback(self, img_bytes: bytes, etiqueta: str) -> str:
        if etiqueta not in CIFAR_LABELS:
            raise HTTPException(400, f"Etiqueta inválida; use una de: {', '.join(CIFAR_LABELS)}.")
        arr = preprocess_image(img_bytes)[0]
        carpeta = os.path.join(self.feedback_dir, etiqueta)
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"{int(time.time() * 1000)}.png")
        Image.fromarray((arr * 255).round().astype("uint8")).save(ruta)
        return ruta

    def cantidad_feedback(self) -> dict:
        return {
            e: len(glob.glob(os.path.join(self.feedback_dir, e, "*.png")))
            for e in CIFAR_LABELS
            if os.path.isdir(os.path.join(self.feedback_dir, e))
        }

    def datos_feedback(self):
        X, y = [], []
        for idx, etiqueta in enumerate(CIFAR_LABELS):
            for ruta in sorted(glob.glob(os.path.join(self.feedback_dir, etiqueta, "*.png"))):
                with open(ruta, "rb") as f:
                    X.append(preprocess_image(f.read())[0])
                y.append(idx)
        if not X:
            raise HTTPException(400, "No hay imágenes de feedback para re-entrenar.")
        return np.stack(X), np.array(y, dtype="int64")

    def datos_repaso(self, cantidad: int, rng):
        """Muestra del conjunto original (focus/, lo guarda el cuaderno 02) para no olvidar lo aprendido."""
        try:
            X = np.load(os.path.join(self.replay_dir, "X_focus.npy"), mmap_mode="r")
            y = np.load(os.path.join(self.replay_dir, "y_focus.npy")).reshape(-1)
        except FileNotFoundError:
            return None
        idx = rng.choice(len(X), size=min(cantidad, len(X)), replace=False)
        return np.asarray(X[idx], dtype="float32"), y[idx].astype("int64")

    def _entrenar(self, epochs, learning_rate, semilla=0):
        from tensorflow import keras

        X, y = self.datos_feedback()
        # Entrenar solo con unas pocas imágenes nuevas hace que el modelo olvide
        # el resto de las clases: se mezclan con 20 ejemplos originales por cada una.
        repaso = self.datos_repaso(20 * len(X), np.random.default_rng(semilla))
        if repaso is not None:
            X, y = np.concatenate([X, repaso[0]]), np.concatenate([y, repaso[1]])

        copia = keras.models.clone_model(self.modelo)
        copia.set_weights(self.modelo.get_weights())
        copia.compile(optimizer=keras.optimizers.Adam(learning_rate), loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])
        historia = copia.fit(X, y, epochs=epochs, batch_size=32, shuffle=True, verbose=0)

        os.makedirs(self.models_dir, exist_ok=True)
        ruta = os.path.join(self.models_dir, f"cnn_model_feedback_{int(time.time())}.keras")
        copia.save(ruta)
        with open(os.path.join(self.models_dir, "latest_model.txt"), "w", encoding="utf-8") as f:
            f.write(ruta)
        return copia, ruta, len(X), float(historia.history["accuracy"][-1])

    async def reentrenar(self, epochs: int, learning_rate: float) -> dict:
        if self._reentrenando.locked():
            raise HTTPException(409, "Ya hay un re-entrenamiento en curso.")
        async with self._reentrenando:
            if self.modelo is None:
                self.cargar()
            # fit bloquea varios segundos: va a otro hilo para no frenar las predicciones.
            copia, ruta, ejemplos, precision = await asyncio.to_thread(self._entrenar, epochs, learning_rate)
            self.usar(copia, ruta)
        return {"modelo": ruta, "ejemplos": ejemplos, "accuracy": round(precision, 3)}


def crear_app(clasificador: Clasificador | None = None) -> FastAPI:
    clf = clasificador or Clasificador()
    app = FastAPI(title="Clasificador CIFAR-10", version="2.0")

    @app.get("/", include_in_schema=False)
    async def inicio():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

    @app.get("/health")
    async def health():
        return {"status": "ok", "modelo": clf.ruta_modelo, "labels": CIFAR_LABELS}

    @app.post("/predict")
    async def predict(file: UploadFile = File(...)):
        etiqueta, confianza, top3 = clf.predecir(await file.read())
        return {
            "pred_label": etiqueta,
            "confidence": round(confianza * 100, 2),
            "top3": [{"label": e, "confidence": round(c * 100, 2)} for e, c in top3],
        }

    @app.post("/feedback")
    async def feedback(true_label: str = Query(...), file: UploadFile = File(...)):
        ruta = clf.guardar_feedback(await file.read(), true_label)
        return {"message": "Feedback guardado", "path": ruta, "por_clase": clf.cantidad_feedback()}

    @app.post("/retrain")
    async def retrain(epochs: int = Query(3, ge=1, le=20), learning_rate: float = Query(1e-4, gt=0, le=0.01)):
        return await clf.reentrenar(epochs, learning_rate)

    return app


app = crear_app()
