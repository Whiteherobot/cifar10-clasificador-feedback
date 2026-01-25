# Proyecto ML con CMM - Clasificacion CIFAR-10

Guia profesional para preparar datos CIFAR-10, entrenar un MLP y ejecutar predicciones en tres cuadernos Jupyter.

---

## Requisitos

- Python 3.10+ (recomendado). Durante la instalacion en Windows, marcar "Add Python to PATH".
- Git (opcional, solo si clonas).
- Windows, macOS o Linux.

---

## Instalacion rapida en Windows (setup.bat / setup.ps1)

1. Descarga o clona el repositorio.
2. Desde el Explorador: doble clic en `setup.bat`. Si no funciona, clic derecho en `setup.ps1` y elige ejecutar con PowerShell.

El script crea `.venv`, instala dependencias y deja listo Jupyter. Tiempo estimado: 5 minutos.

---

## Instalacion manual

1. Crear entorno virtual
    - Windows: `py -m venv .venv` y luego `.venv\Scripts\activate`
    - macOS/Linux: `python3 -m venv .venv` y luego `source .venv/bin/activate`
2. Instalar dependencias: `pip install --upgrade pip` y `pip install -r requirements.txt`
3. Iniciar Jupyter: `jupyter notebook` y abrir http://localhost:8888

---

## Estructura del proyecto

```
README.md
requirements.txt
setup.bat / setup.ps1
.venv/ (generado)
01_preparacion_dataset.ipynb
02_modelado_entrenamiento_cmm.ipynb
03_pruebas_y_predicciones.ipynb
data/ (generado: *.npz, test_images/)
models/ (generado: model_*.joblib, *_meta.joblib)
utils/transform.py
```

---

## Flujo recomendado (orden de ejecucion)

1. Preparar dataset: ejecutar `01_preparacion_dataset.ipynb`
    - Descarga CIFAR-10, normaliza y guarda `data/*.npz`.
2. Entrenar modelo: ejecutar `02_modelado_entrenamiento_cmm.ipynb`
    - Carga NPZ, entrena `MLPClassifier` (1024, 512, 256) con early stopping, guarda `models/model_<ts>.joblib` y metadatos.
3. Probar predicciones: ejecutar `03_pruebas_y_predicciones.ipynb`
    - Carga el ultimo modelo, procesa imagenes en `data/test_images/` y muestra predicciones CIFAR-10.

---

## Uso de los cuadernos

- Cuaderno 1: genera `cifar10_raw.npz`, `processed_cifar10.npz`, `historical.npz`, `new_samples.npz`.
- Cuaderno 2: entrena MLP con capas (1024, 512, 256), `learning_rate_init=5e-4`, `alpha=1e-4`, entrenamiento incremental y early stopping; versiona el mejor checkpoint.
- Cuaderno 3: redimensiona a 32x32 RGB, aplica el transformador guardado (o normalizacion simple), predice y muestra grilla de imagenes; exporta `data/predictions_images.csv` y `data/predictions_images.npz`.

---

## Resultados esperados (referencia)

- Entrenamiento: accuracy de validacion aproximada 50-70% con imagenes aplanadas.
- Prediccion: cuadrilla de imagenes con etiqueta CIFAR-10 y CSV/NPZ de resultados.

---

## Solucion de problemas

- Falta dataset procesado: ejecutar el cuaderno 1 completo.
- No hay modelos en `models/`: ejecutar el cuaderno 2 completo.
- Jupyter no abre: `jupyter notebook --ip=127.0.0.1 --port=8888`.
- TensorFlow ausente: `pip install --upgrade -r requirements.txt`.

---

## Requerimientos tecnicos

- Minimo: 4 GB RAM, CPU dual-core, 500 MB libres.
- Recomendado: 8 GB RAM, CPU quad-core; GPU opcional acelera TensorFlow.

---

## Contacto

Si necesitas soporte, verifica primero la seccion de solucion de problemas y la configuracion del entorno (Python 3.10+, entorno virtual activado, dependencias instaladas).
- [ ] Cuaderno 01 ejecutado completamente
- [ ] Cuaderno 02 ejecutado completamente
- [ ] Imágenes copiadas a `data/test_images/` (opcional)
- [ ] Cuaderno 03 ejecutado completamente
- [ ] Modelos guardados en `models/` verificados

---

**¡Proyecto listo para evaluar! 🎉**

*Última actualización: Enero 2026*
