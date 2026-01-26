# Información sobre archivos excluidos de Git

## 📦 ¿Qué archivos NO se suben a Git?

Este proyecto está configurado para **NO versionar archivos pesados** que se generan durante el entrenamiento.

### ❌ Archivos Excluidos (en .gitignore)

#### 1. Datasets Procesados (data/)
- `data/*.npz` (~200-300 MB total)
  - cifar10_raw.npz
  - processed_cifar10.npz
  - historical.npz
  - new_samples.npz
- `data/*.csv` (predicciones)
- `data/test_images/*.jpg` (imágenes de prueba)

**Razón:** Archivos muy pesados, se regeneran ejecutando el cuaderno 01

#### 2. Modelos Entrenados (models/)
- `models/*.joblib` (~50-100 MB por modelo)
  - model_<timestamp>.joblib
  - model_<timestamp>_meta.joblib
  - model_retrained_<timestamp>.joblib
- `models/latest_model.txt`

**Razón:** Archivos muy pesados, se regeneran ejecutando el cuaderno 02

#### 3. Dataset de Reentrenamiento (focus/)
- `focus/*.npy` (~200 MB)
  - X_focus.npy
  - y_focus.npy

**Razón:** Archivos muy pesados, se regeneran ejecutando el cuaderno 02

#### 4. Entorno Virtual
- `.venv/` (cientos de MB)
- `__pycache__/`
- `*.pyc`, `*.pyo`, `*.pyd`

**Razón:** Se recrea con `python -m venv .venv` e instalando requirements.txt

---

## ✅ ¿Qué SÍ se sube a Git?

### Código Fuente
- ✅ `01_preparacion_dataset.ipynb`
- ✅ `02_modelado_entrenamiento_cmm.ipynb`
- ✅ `03_pruebas_y_predicciones.ipynb`
- ✅ `utils/transform.py`
- ✅ `run_pipeline.py`

### Configuración
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `INICIO_RAPIDO.md`
- ✅ `setup.bat` / `setup.ps1`
- ✅ `start_jupyter.bat` / `start_jupyter.ps1`
- ✅ `.gitignore`

### Estructura (archivos .gitkeep)
- ✅ `data/.gitkeep`
- ✅ `models/.gitkeep`
- ✅ `focus/.gitkeep`
- ✅ `data/test_images/.gitkeep`

**Razón:** Mantiene la estructura de carpetas sin subir archivos pesados

---

## 🔄 Cómo Replicar el Proyecto en Otro Equipo

```powershell
# 1. Clonar repositorio
git clone <tu-repo-url>
cd iaJordy

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 5. Ejecutar cuadernos en orden
.\start_jupyter.bat
# Luego ejecutar: 01 → 02 → 03
```

Los archivos pesados (data/, models/, focus/) se regenerarán automáticamente.

---

## 📊 Tamaños Aproximados

| Archivo/Carpeta | Tamaño | ¿En Git? |
|----------------|--------|----------|
| data/*.npz | ~300 MB | ❌ No |
| models/*.joblib | ~100 MB/modelo | ❌ No |
| focus/*.npy | ~200 MB | ❌ No |
| .venv/ | ~500 MB | ❌ No |
| Código fuente | ~2 MB | ✅ Sí |
| **Total en Git** | **~2 MB** | ✅ Sí |
| **Total local** | **~1.1 GB** | - |

---

## 💡 Ventajas de Esta Configuración

1. **Repositorio ligero**: Solo ~2 MB en Git
2. **Rápido para clonar**: Descarga instantánea
3. **Reproducible**: Cualquiera puede regenerar los archivos
4. **Colaboración eficiente**: No conflictos con archivos binarios grandes
5. **Sin cuota**: No llena el límite de almacenamiento de Git

---

## 🛡️ Seguridad

Los archivos excluidos **NO incluyen información sensible**, solo:
- Datasets públicos (CIFAR-10)
- Modelos entrenados (reproducibles)
- Archivos temporales

Si necesitas versionar modelos específicos, considera usar **Git LFS** (Large File Storage).

---

**Última actualización:** 25/01/2026
