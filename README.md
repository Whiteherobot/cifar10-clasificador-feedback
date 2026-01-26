# CIFAR-10: Notebooks + Web/API (FastAPI)

Guía única para levantar el proyecto desde los cuadernos (Jupyter) y hasta la demo web con FastAPI + HTML estático.

## 1. Requisitos
- Python 3.10+ (64-bit recomendado)
- Windows/macOS/Linux
- (Opcional) Git

## 2. Instalación rápida
### Windows
```powershell
py -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Uso con cuadernos Jupyter (pipeline completo)
1) **Arrancar Jupyter**
```bash
jupyter notebook
```
2) **Cuaderno 01 – Preparación de datos** (`01_preparacion_dataset.ipynb`)
  - Descarga CIFAR-10, normaliza y guarda splits (`data/*.npz`).
3) **Cuaderno 02 – Entrenamiento** (`02_modelado_entrenamiento_cmm.ipynb`)
  - Entrena la CNN optimizada y genera `models/cnn_model_*.keras` + `models/latest_model.txt`.
  - Guarda dataset focal para fine-tuning en `focus/X_focus.npy` y `focus/y_focus.npy`.
4) **Cuaderno 03 – Pruebas y fine-tuning** (`03_pruebas_y_predicciones.ipynb`)
  - Coloca imágenes en `data/test_images/` (o usa la celda para crear `data/test_images_32x32`).
  - Ejecuta predicciones, analiza top-3/confianza y ejecuta fine-tuning por clases si lo necesitas.

## 4. Uso del servidor FastAPI + UI web
1) **Activar entorno**
```powershell
# Windows
.\.venv\Scripts\activate
```
```bash
# macOS/Linux
source .venv/bin/activate
```
2) **Iniciar servidor**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
3) **Abrir la UI**
- Navega a http://localhost:8000
- Carga varias imágenes y pulsa "Predecir todo".
- Haz clic en la tarjeta mal predicha, escribe la etiqueta correcta y envía feedback.
- Opcional: ejecuta "Reentrenar" (usa feedback guardado en `data/feedback/`).
4) **API Docs**
- Swagger: http://localhost:8000/docs
- Endpoints clave:
  - `POST /predict` (file)
  - `POST /feedback` (true_label + file)
  - `POST /retrain` (epochs, learning_rate)
  - `GET /health`

## 5. Estructura mínima
```
README.md
requirements.txt
main.py                  # FastAPI
static/index.html        # UI
01_preparacion_dataset.ipynb
02_modelado_entrenamiento_cmm.ipynb
03_pruebas_y_predicciones.ipynb
models/                  # cnn_model_*.keras, latest_model.txt
focus/                   # X_focus.npy, y_focus.npy
data/
  test_images/
  test_images_32x32/
  feedback/<label>/
```

## 6. Flujo sugerido
- Primera vez: Cuaderno 01 → Cuaderno 02 → probar en Cuaderno 03.
- Para demo web: tener al menos un modelo en `models/` (creado en Cuaderno 02) y arrancar FastAPI.
- Para mejorar con feedback: usar la UI o `/feedback`, luego `/retrain`.

## 7. Problemas comunes
- **"No se encontró modelo"**: ejecuta Cuaderno 02 para crear `models/cnn_model_*.keras` y `models/latest_model.txt`.
- **Sin datos de feedback para reentrenar**: envía ejemplos a `/feedback` (se guardan en `data/feedback/<label>/`).
- **Imágenes fuera de 32×32**: la UI reescala; para mejores resultados usa la celda de preprocesado en Cuaderno 03.
- **Puerto ocupado**: cambia a `--port 8001`.

## 8. Comandos cortos
```bash
# Activar venv (Windows)
.\.venv\Scripts\activate
# Activar venv (macOS/Linux)
source .venv/bin/activate
# Servidor FastAPI
python -m uvicorn main:app --reload --port 8000
# Jupyter Notebook
jupyter notebook
```

Listo: con esto puedes ir de los cuadernos a la demo web y reentrenar usando feedback.

1. Revisa la sección de Solución de Problemas
2. Verifica el Checklist de Verificación
3. Consulta los comentarios en los cuadernos
4. Revisa los metadatos de los modelos guardados

**Configuración del entorno:**
- Python 3.10+
- Entorno virtual activado
- Dependencias instaladas según `requirements.txt`

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos y de investigación.

---

**¡Feliz entrenamiento! 🎯**