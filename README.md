# cifar10-clasificador-feedback

[![CI](https://github.com/Whiteherobot/cifar10-clasificador-feedback/actions/workflows/ci.yml/badge.svg)](https://github.com/Whiteherobot/cifar10-clasificador-feedback/actions/workflows/ci.yml)

Clasificador de imágenes de CIFAR-10 (avión, auto, pájaro, gato, ciervo, perro,
rana, caballo, barco y camión) con una CNN en Keras, servido con FastAPI. Desde
la página se suben imágenes, se corrigen las predicciones equivocadas y se
re-entrena el modelo con esas correcciones. Proyecto de Inteligencia Artificial
(enero de 2026), hecho en pareja.

## Cuadernos

| Cuaderno | Qué hace |
|---|---|
| `01_preparacion_dataset.ipynb` | Descarga CIFAR-10, normaliza y guarda los conjuntos en `data/`. |
| `02_modelado_entrenamiento_cmm.ipynb` | Entrena la CNN (bloques convolucionales con batch normalization y dropout, aumento de datos). Llega a 84 % de accuracy en validación (12 000 imágenes). Guarda el modelo en `models/` y una muestra del conjunto en `focus/`. |
| `03_pruebas_y_predicciones.ipynb` | Prueba el modelo con imágenes nuevas, analiza el top 3 y la accuracy por clase. |

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-cuadernos.txt
jupyter notebook
```

Los cuadernos se dejaron con sus salidas. Los modelos y datos que generan no
están en el repo (pesan cientos de MB).

## API y página

Con un modelo entrenado en `models/`:

```bash
pip install -r requirements.txt
uvicorn main:app --reload      # http://localhost:8000
```

| Método | Ruta | |
|---|---|---|
| POST | `/predict` | Imagen (cualquier tamaño, se lleva a 32×32) → clase, confianza y top 3. |
| POST | `/feedback?true_label=cat` | Guarda la imagen con su clase correcta en `data/feedback/`. |
| POST | `/retrain?epochs=3&learning_rate=0.0001` | Re-entrena con el feedback y pasa a usar el modelo nuevo. |
| GET | `/health` | Modelo en uso. |

El re-entrenamiento no usa solo las imágenes corregidas: con unas pocas, el
modelo aprende esas y olvida el resto. Por cada imagen de feedback mezcla 20
ejemplos del conjunto original (`focus/`). Se entrena una copia en otro hilo,
así las predicciones siguen funcionando con el modelo anterior hasta que la
copia termina.

## Pruebas

```bash
pip install pytest httpx
pytest
```

Usan una CNN mínima sin entrenar para recorrer la API: predicción, imágenes
inválidas, feedback, re-entrenamiento con datos de repaso, parámetros fuera de
rango y la falta de modelo.

## De dónde sale

En 2026 se limpió el repo (antes `iaJordy`): tenía 19 modelos de 33 MB cada uno,
los datos generados, las imágenes de feedback, cinco archivos de notas de la
sesión de trabajo y un `requirements.txt` de 133 paquetes en UTF-16 que no se
podía instalar fuera de Windows. También se corrigió el re-entrenamiento (que
hacía olvidar al modelo y bloqueaba la API mientras entrenaba) y se agregaron
pruebas y CI.

## Autores

- Michael Lata ([@Whiteherobot](https://github.com/Whiteherobot))
- Jordy Romero ([@JordyRomeroa](https://github.com/JordyRomeroa))

Licencia MIT.
