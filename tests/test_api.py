import os
from io import BytesIO

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from tensorflow import keras

from main import CIFAR_LABELS, Clasificador, crear_app


def modelo_chico():
    """CNN mínima con la misma entrada y salida que la del proyecto (sin entrenar)."""
    keras.utils.set_random_seed(0)
    modelo = keras.Sequential([
        keras.Input((32, 32, 3)),
        keras.layers.Conv2D(4, 3, activation="relu"),
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(10, activation="softmax"),
    ])
    return modelo


def png(color=(200, 30, 30), tamano=(64, 48)):
    buf = BytesIO()
    Image.new("RGB", tamano, color).save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def entorno(tmp_path):
    clf = Clasificador(models_dir=str(tmp_path / "models"), feedback_dir=str(tmp_path / "feedback"),
                       replay_dir=str(tmp_path / "focus"))
    clf.usar(modelo_chico())
    return clf, TestClient(crear_app(clf)), tmp_path


def test_predice_con_el_top3_ordenado(entorno):
    _, cliente, _ = entorno
    r = cliente.post("/predict", files={"file": ("rojo.png", png(), "image/png")})
    assert r.status_code == 200
    datos = r.json()
    assert datos["pred_label"] in CIFAR_LABELS
    assert len(datos["top3"]) == 3
    assert datos["top3"][0]["confidence"] >= datos["top3"][1]["confidence"] >= datos["top3"][2]["confidence"]
    assert datos["confidence"] == datos["top3"][0]["confidence"]


def test_rechaza_archivos_que_no_son_imagenes(entorno):
    _, cliente, _ = entorno
    assert cliente.post("/predict", files={"file": ("x.txt", b"hola", "text/plain")}).status_code == 400
    assert cliente.post("/feedback?true_label=llama", files={"file": ("a.png", png(), "image/png")}).status_code == 400


def test_feedback_se_guarda_a_32x32_en_la_carpeta_de_su_clase(entorno):
    clf, cliente, tmp = entorno
    r = cliente.post("/feedback?true_label=ship", files={"file": ("barco.png", png((20, 60, 200)), "image/png")})
    assert r.status_code == 200
    assert r.json()["por_clase"] == {"ship": 1}
    guardada = Image.open(r.json()["path"])
    assert guardada.size == (32, 32)


def test_reentrena_una_copia_y_la_mezcla_con_datos_originales(entorno):
    clf, cliente, tmp = entorno
    for _ in range(3):
        cliente.post("/feedback?true_label=ship", files={"file": ("b.png", png((20, 60, 200)), "image/png")})
    os.makedirs(tmp / "focus")
    rng = np.random.default_rng(0)
    np.save(tmp / "focus" / "X_focus.npy", rng.random((100, 32, 32, 3), dtype=np.float32))
    np.save(tmp / "focus" / "y_focus.npy", rng.integers(0, 10, 100))

    anterior = clf.modelo
    r = cliente.post("/retrain?epochs=1")
    assert r.status_code == 200
    datos = r.json()
    assert datos["ejemplos"] == 3 + 60  # 3 de feedback + 20 originales por cada una
    assert clf.modelo is not anterior  # el modelo viejo no se tocó: se entrenó una copia
    assert os.path.exists(datos["modelo"])
    assert open(tmp / "models" / "latest_model.txt").read() == datos["modelo"]
    assert cliente.get("/health").json()["modelo"] == datos["modelo"]


def test_sin_feedback_no_reentrena_y_valida_parametros(entorno):
    _, cliente, _ = entorno
    assert cliente.post("/retrain").status_code == 400
    assert cliente.post("/retrain?epochs=0").status_code == 422
    assert cliente.post("/retrain?learning_rate=5").status_code == 422


def test_sin_modelo_responde_503(tmp_path):
    cliente = TestClient(crear_app(Clasificador(models_dir=str(tmp_path))))
    assert cliente.post("/predict", files={"file": ("a.png", png(), "image/png")}).status_code == 503


def test_sirve_la_pagina(entorno):
    _, cliente, _ = entorno
    assert "CIFAR" in cliente.get("/").text
