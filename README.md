# Proyecto ML con CMM - CIFAR-10 Classification

## 📋 Descripción del Proyecto

Sistema de clasificación de imágenes CIFAR-10 usando Machine Learning incremental con `MLPClassifier` (Red Neuronal). El proyecto implementa un flujo completo de ML: **Preparación de datos → Entrenamiento → Predicción** en tres cuadernos independientes.

**Dataset:** CIFAR-10 (60,000 imágenes RGB 32×32, 10 clases)  
**Modelo:** MLPClassifier con capas (1024, 512, 256) neuronas  
**Accuracy esperada:** 50-70% (lineal en imágenes aplanadas)

---

## 🚀 Instalación Rápida (5 minutos)

### Requisitos Previos
- **Python 3.10+** (recomendado 3.10.0) - Descarga desde https://www.python.org/downloads/
  - ⚠️ **IMPORTANTE:** Marca "Add Python to PATH" durante la instalación
- **Windows / macOS / Linux**
- **Git** (opcional, solo para clonar)

---

## ⚡ OPCIÓN RÁPIDA: Ejecutable Automático (RECOMENDADO)

### Windows - Doble Click Setup

**Paso 1:** Descargar el proyecto

```bash
# Opción A: Clonar
git clone <repo-url>
cd "New folder"

# Opción B: Descargar ZIP y descomprimir la carpeta
```

**Paso 2:** Ejecutar instalador

```bash
# Opción A: BATCH (más simple)
Doble-click en: setup.bat

# Opción B: PowerShell (si .bat no funciona)
Click derecho en setup.ps1 → "Run with PowerShell"
```

**¡Eso es todo! El script hará:**
- ✅ Verificar Python
- ✅ Crear virtual environment
- ✅ Instalar todas las dependencias (3-5 min)
- ✅ Crear carpetas necesarias
- ✅ Iniciar Jupyter automáticamente (opcional)

**Tiempo total:** ~5 minutos

---

## 📋 Instalación Manual (si el ejecutable no funciona)

### Paso 1: Descargar el Proyecto

```bash
# Opción A: Clonar (si tienes Git)
git clone <repo-url>
cd "New folder"

# Opción B: Descargar ZIP y descomprimir
# Luego abrir la carpeta en terminal
```

### Paso 2: Crear Virtual Environment

```bash
# Windows (Cmd o PowerShell)
py -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencias principales:**
- numpy, pandas, scikit-learn, tensorflow, jupyter, matplotlib, pillow

**Tiempo esperado:** ~3-5 minutos

### Paso 4: Iniciar Jupyter

```bash
jupyter notebook
```

Abre http://localhost:8888 en tu navegador.

---

## 📊 Estructura del Proyecto

```
New folder/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias
├── setup.bat                          # 🚀 Instalador automático (Windows)
├── setup.ps1                          # 🚀 Instalador PowerShell (alternativa)
├── .venv/                             # Virtual environment (generado)
│
├── 01_preparacion_dataset.ipynb       # Cargar CIFAR-10, EDA, split
├── 02_modelado_entrenamiento_cmm.ipynb  # Entrenar MLPClassifier (35 epochs)
├── 03_pruebas_y_predicciones.ipynb   # Cargar imágenes, predecir
│
├── data/                              # Datos (generado)
│   ├── cifar10_raw.npz
│   ├── processed_cifar10.npz
│   ├── historical.npz
│   ├── new_samples.npz
│   └── test_images/                   # Coloca aquí tus imágenes JPG/PNG
│
├── models/                            # Modelos entrenados (generado)
│   ├── model_<timestamp>.joblib       # Modelo serializado
│   └── model_<timestamp>_meta.joblib  # Metadatos
│
└── utils/
    └── transform.py                   # Funciones de transformación
```

---

## 📖 Ejecución de los Cuadernos

### Cuaderno 1: Preparación del Dataset
**Archivo:** `01_preparacion_dataset.ipynb`

**Qué hace:**
- Descarga CIFAR-10 desde TensorFlow/Keras
- Análisis exploratorio (EDA): distribución de clases, shape, etc.
- Normaliza imágenes (÷255) y aplana a 1D (3072 features)
- Divide en train/test y guarda NPZ

**Salida:**
- `data/cifar10_raw.npz`
- `data/processed_cifar10.npz`
- `data/historical.npz`
- `data/new_samples.npz`

**Tiempo:** ~2-3 minutos

**Pasos:**
1. Abre el cuaderno
2. Ejecuta celdas en orden (Shift+Enter)
3. Espera a que termine

---

### Cuaderno 2: Entrenamiento del Modelo
**Archivo:** `02_modelado_entrenamiento_cmm.ipynb`

**Qué hace:**
- Carga datos procesados del cuaderno 1
- Inicializa `MLPClassifier` (1024, 512, 256 neuronas)
- Entrena 35 epochs con mini-batch (batch_size=128)
- Early stopping si val_accuracy no mejora por 15 epochs
- Guarda modelo versionado con timestamp

**Hyperparámetros:**
- `hidden_layers`: (1024, 512, 256)
- `solver`: adam
- `learning_rate`: adaptive
- `learning_rate_init`: 5e-4
- `alpha`: 1e-4 (L2 regularization)
- `epochs`: 35 (early stopping puede detener antes)

**Salida:**
- `models/model_<timestamp>.joblib` (modelo)
- `models/model_<timestamp>_meta.joblib` (metadata)
- Accuracy mostrado en cada epoch

**Tiempo:** ~5-10 minutos

**Expected Accuracy:**
- Train: 60-75%
- Val: 50-70%

**Pasos:**
1. Ejecuta cuaderno 1 primero
2. Abre este cuaderno
3. Ejecuta celdas en orden
4. Observa el progreso de epochs

---

### Cuaderno 3: Predicciones con Imágenes Personalizadas
**Archivo:** `03_pruebas_y_predicciones.ipynb`

**Qué hace:**
- Carga el último modelo guardado
- Crea carpeta `data/test_images` si no existe
- Lee imágenes JPG/PNG de esa carpeta
- Redimensiona a 32×32 RGB
- Aplica transformación (normaliza, aplana)
- Predice clase CIFAR-10 para cada imagen
- Muestra imágenes con predicciones en una cuadrícula

**Clases CIFAR-10:**
```
0: airplane       5: dog
1: automobile     6: frog
2: bird           7: horse
3: cat            8: ship
4: deer           9: truck
```

**Cómo usar:**
1. Coloca imágenes JPG/PNG en `data/test_images/`
2. Abre el cuaderno
3. Ejecuta celdas en orden
4. Ver predicciones visualizadas

**Tiempo:** ~30 segundos (sin contar descargas)

---

## 🎯 Flujo Completo Recomendado

```
1. SETUP (Paso 1-4 arriba)
   └─> pip install -r requirements.txt
       jupyter notebook

2. PREPARACIÓN
   └─> Ejecutar: 01_preparacion_dataset.ipynb
       └─> Genera: data/*.npz

3. ENTRENAMIENTO
   └─> Ejecutar: 02_modelado_entrenamiento_cmm.ipynb
       └─> Genera: models/model_*.joblib

4. PREDICCIÓN
   ├─> Copiar imágenes a data/test_images/
   └─> Ejecutar: 03_pruebas_y_predicciones.ipynb
       └─> Muestra: imágenes + predicciones
```

**Tiempo total:** ~15 minutos (primera ejecución)

---

## 📸 Probando con Imágenes Propias

### Opción 1: Usar imágenes locales
```bash
# Copia tus imágenes a:
data/test_images/
├── imagen1.jpg
├── imagen2.png
├── foto_animales.jpg
└── ...
```

Ejecuta cuaderno 03 → Verá predicciones CIFAR-10

### Opción 2: Descargar imágenes de ejemplo
```bash
# Desde terminal (Windows)
mkdir data\test_images
# Descarga imágenes JPG a esa carpeta
```

---

## ⚙️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'tensorflow'"

```bash
# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### Error: "FileNotFoundError: No se encuentra dataset procesado"

**Solución:** Ejecuta primero `01_preparacion_dataset.ipynb` completo

### Error: "No se encontró ningún modelo en models/"

**Solución:** Ejecuta primero `02_modelado_entrenamiento_cmm.ipynb` completo

### Jupyter no abre

```bash
# Reinicia Jupyter
jupyter notebook --ip=127.0.0.1 --port=8888
```

### Lento en predicción

- Normal: MLPClassifier es lento en CPU
- Espera 30-60 segundos por imagen en primeras ejecuciones

---

## 📊 Resultados Esperados

### Cuaderno 1 (Preparación)
```
✅ Cifar10 dataset loaded: (60000, 3072)
✅ Train/Val split: 48000/12000
✅ Files saved: historical.npz, new_samples.npz
```

### Cuaderno 2 (Entrenamiento)
```
Entrenamiento intensivo: 35 epochs, batch_size=128

Epoch   1/35 -> Train Acc: 35.27% | Train Loss: 1.8230 | Val Acc: 31.12%
Epoch   5/35 -> Train Acc: 48.15% | Train Loss: 1.5420 | Val Acc: 44.33%
Epoch  10/35 -> Train Acc: 58.42% | Train Loss: 1.1870 | Val Acc: 53.21%
...
Epoch  35/35 -> Train Acc: 72.50% | Train Loss: 0.6234 | Val Acc: 65.80%

------------------------------
RESULTADO FINAL:
Train Accuracy: 0.7250 (72.50%)
Val Accuracy:   0.6580 (65.80%)

💾 Modelo guardado:
   Modelo: models/model_1705382941.joblib
   Metadata: models/model_1705382941_meta.joblib
```

### Cuaderno 3 (Predicción)
```
✅ Procesamiento completado: 5 imágenes

[Muestra cuadrícula 3x2 con imágenes y predicciones]
gato.jpg → Predicción: CAT (Clase 3)
perro.jpg → Predicción: DOG (Clase 5)
...
```

---

## 🔧 Requerimientos Técnicos

### Hardware mínimo
- RAM: 4 GB
- CPU: Dual-core (Core i5 equivalente)
- Almacenamiento: 500 MB

### Hardware recomendado
- RAM: 8 GB
- CPU: Quad-core (Core i7 equivalente)
- GPU: Opcional (acelera TensorFlow)

---

## 📝 Notas Académicas

### Arquitectura del Modelo
- **Tipo:** MLPClassifier (scikit-learn)
- **Capas:** Input (3072) → [1024] → [512] → [256] → Output (10 clases)
- **Activación:** ReLU
- **Optimizer:** Adam
- **Loss:** Cross-entropy (log_loss)

### Limitaciones
- Imágenes aplanadas pierden información espacial (ideal sería CNN)
- SGDClassifier inicial cambió a MLPClassifier para mejor rendimiento
- Entrenamiento incremental (partial_fit) para demostrar aprendizaje online
- Accuracy limitada por representación lineal de características

### Justificación de 35 Epochs
- Early stopping detiene si no mejora
- 35 es máximo razonable sin overfitting excesivo
- Cada epoch procesa dataset completo en mini-batches

---

## 📞 Contacto / Soporte

Si tienes problemas:
1. Revisa "[Solución de Problemas](#solución-de-problemas)"
2. Verifica que Python 3.10+ esté instalado: `python --version`
3. Confirma virtual env activo: `pip list` debe mostrar paquetes

---

## ✅ Checklist para el Evaluador

- [ ] Python 3.10+ instalado
- [ ] Virtual environment creado y activado
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] `jupyter notebook` iniciado
- [ ] Cuaderno 01 ejecutado completamente
- [ ] Cuaderno 02 ejecutado completamente
- [ ] Imágenes copiadas a `data/test_images/` (opcional)
- [ ] Cuaderno 03 ejecutado completamente
- [ ] Modelos guardados en `models/` verificados

---

**¡Proyecto listo para evaluar! 🎉**

*Última actualización: Enero 2026*
