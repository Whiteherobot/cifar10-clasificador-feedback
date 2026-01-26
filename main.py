import asyncio
import glob
import os
import time
from io import BytesIO
from typing import List, Tuple

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from tensorflow import keras

# CIFAR-10 labels used by the trained CNN
CIFAR_LABELS = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck",
]

# Directories
MODELS_DIR = "models"
FEEDBACK_DIR = os.path.join("data", "feedback")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

os.makedirs(FEEDBACK_DIR, exist_ok=True)

app = FastAPI(title="CIFAR-10 Demo API", version="1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------------------------------------------------------------------------
# Model loading helpers
# ---------------------------------------------------------------------------

def _find_latest_model_path() -> str:
    """Return path to the latest .keras model, honoring models/latest_model.txt."""
    latest_txt = os.path.join(MODELS_DIR, "latest_model.txt")
    if os.path.exists(latest_txt):
        with open(latest_txt, "r", encoding="utf-8") as f:
            candidate = f.read().strip()
        if candidate and os.path.exists(candidate):
            return candidate
    keras_files = glob.glob(os.path.join(MODELS_DIR, "*.keras"))
    if not keras_files:
        raise FileNotFoundError("No CNN model found in models/. Ejecuta el cuaderno 02 primero.")
    return max(keras_files, key=os.path.getmtime)


def load_model() -> keras.Model:
    model_path = _find_latest_model_path()
    model = keras.models.load_model(model_path)
    return model


# The global model instance used for inference
model = load_model()
model_lock = asyncio.Lock()


# ---------------------------------------------------------------------------
# Image utilities
# ---------------------------------------------------------------------------

def preprocess_image(img_bytes: bytes) -> np.ndarray:
    """Convert raw bytes to a normalized tensor shaped (1, 32, 32, 3)."""
    try:
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Error al leer la imagen: {exc}") from exc

    if img.size != (32, 32):
        img = img.resize((32, 32), Image.LANCZOS)

    arr = np.array(img, dtype="float32") / 255.0
    return arr.reshape(1, 32, 32, 3)


def predict_image(img_bytes: bytes) -> Tuple[str, float, List[Tuple[str, float]]]:
    """Run model prediction and return (label, confidence, top3 list)."""
    global model
    x = preprocess_image(img_bytes)
    probs = model.predict(x, verbose=0)[0]
    top3_idx = np.argsort(probs)[-3:][::-1]
    top3 = [(CIFAR_LABELS[i], float(probs[i])) for i in top3_idx]
    best_label, best_conf = top3[0]
    return best_label, best_conf, top3


# ---------------------------------------------------------------------------
# Feedback and retraining helpers
# ---------------------------------------------------------------------------

def save_feedback_image(img_bytes: bytes, true_label: str) -> str:
    """Persist feedback image under data/feedback/<label>/timestamp.png."""
    if true_label not in CIFAR_LABELS:
        raise HTTPException(status_code=400, detail="Etiqueta inválida. Usa labels CIFAR-10.")
    label_dir = os.path.join(FEEDBACK_DIR, true_label)
    os.makedirs(label_dir, exist_ok=True)
    ts = int(time.time() * 1000)
    filename = f"{ts}.png"
    path = os.path.join(label_dir, filename)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    if img.size != (32, 32):
        img = img.resize((32, 32), Image.LANCZOS)
    img.save(path, format="PNG")
    return path


def load_feedback_dataset() -> Tuple[np.ndarray, np.ndarray]:
    """Load all feedback images into tensors and label indices."""
    X_list: List[np.ndarray] = []
    y_list: List[int] = []
    for idx, label in enumerate(CIFAR_LABELS):
        label_dir = os.path.join(FEEDBACK_DIR, label)
        if not os.path.isdir(label_dir):
            continue
        for fname in os.listdir(label_dir):
            if not fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                continue
            fpath = os.path.join(label_dir, fname)
            try:
                with open(fpath, "rb") as f:
                    arr = preprocess_image(f.read())
                X_list.append(arr[0])
                y_list.append(idx)
            except Exception:
                continue
    if not X_list:
        raise HTTPException(status_code=400, detail="No hay datos de feedback para reentrenar.")
    X = np.stack(X_list, axis=0)
    y = np.array(y_list, dtype="int64")
    return X, y


async def fine_tune_from_feedback(epochs: int = 3, learning_rate: float = 1e-4) -> str:
    """Fine-tune the current model using feedback images."""
    global model
    X, y = load_feedback_dataset()

    async with model_lock:
        compiled = bool(model.optimizer)
        if not compiled:
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"],
            )
        history = model.fit(
            X,
            y,
            validation_split=0.2,
            epochs=epochs,
            batch_size=32,
            verbose=1,
        )
        ts = int(time.time())
        out_path = os.path.join(MODELS_DIR, f"cnn_model_feedback_{ts}.keras")
        model.save(out_path)
        with open(os.path.join(MODELS_DIR, "latest_model.txt"), "w", encoding="utf-8") as f:
            f.write(out_path)
    last_acc = history.history.get("accuracy", [0])[-1]
    last_val = history.history.get("val_accuracy", [0])[-1]
    return f"Modelo guardado en {out_path} (acc={last_acc:.3f}, val_acc={last_val:.3f})"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": True, "labels": CIFAR_LABELS}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No se adjuntó archivo")
    img_bytes = await file.read()
    label, conf, top3 = predict_image(img_bytes)
    return {
        "pred_label": label,
        "confidence": round(conf * 100, 2),
        "top3": [{"label": l, "confidence": round(c * 100, 2)} for l, c in top3],
    }


@app.post("/feedback")
async def feedback(true_label: str, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No se adjuntó archivo")
    img_bytes = await file.read()
    saved_path = save_feedback_image(img_bytes, true_label)
    return {"message": "Feedback guardado", "path": saved_path}


@app.post("/retrain")
async def retrain(epochs: int = 3, learning_rate: float = 1e-4):
    info = await fine_tune_from_feedback(epochs=epochs, learning_rate=learning_rate)
    return {"message": info}


@app.exception_handler(FileNotFoundError)
async def handle_not_found(_, exc: FileNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def handle_generic(_, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
