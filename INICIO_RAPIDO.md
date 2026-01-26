# ====================================================
# GUÍA DE INICIO RÁPIDO - Proyecto CIFAR-10
# ====================================================

## 🚀 TODO ESTÁ LISTO PARA USAR

Tu entorno ya está completamente configurado:
- ✅ Entorno virtual Python 3.10 creado (.venv/)
- ✅ Todas las dependencias instaladas
- ✅ Estructura de carpetas lista
- ✅ .gitignore configurado

---

## 📝 CÓMO INICIAR

### Opción 1: Doble clic (más fácil)
1. Doble clic en `start_jupyter.bat`
2. Se abrirá Jupyter en tu navegador
3. ¡Listo para trabajar!

### Opción 2: PowerShell
```powershell
.\start_jupyter.ps1
```

### Opción 3: Manual
```powershell
.\.venv\Scripts\Activate.ps1
jupyter notebook
```

---

## 📚 ORDEN DE EJECUCIÓN

### 1️⃣ Preparar Dataset
Abre: `01_preparacion_dataset.ipynb`
- Ejecuta todas las celdas (Cell → Run All)
- Tiempo: ~2-3 minutos
- Salida: Archivos .npz en data/

### 2️⃣ Entrenar Modelo
Abre: `02_modelado_entrenamiento_cmm.ipynb`
- Ejecuta todas las celdas
- Tiempo: ~15-25 minutos
- Objetivo: >80% accuracy
- Salida: Modelos en models/, dataset en focus/

### 3️⃣ Predicciones y Mejora
Abre: `03_pruebas_y_predicciones.ipynb`
- Coloca imágenes en data/test_images/
- Ejecuta celdas de predicción
- Si detectas clases con baja accuracy:
  - Ajusta CLASSES_TO_RETRAIN
  - Ejecuta celda de reentrenamiento
- Salida: Predicciones y modelo mejorado

---

## 📦 ARCHIVOS VERSIONADOS vs IGNORADOS

### ✅ Versionados (suben a Git)
- Notebooks (.ipynb)
- Código fuente (utils/*.py)
- Configuración (requirements.txt, README.md)
- Estructura vacía (.gitkeep)

### ❌ Ignorados (NO suben a Git)
- data/*.npz (datasets procesados - pesados)
- models/*.joblib (modelos entrenados - muy pesados)
- focus/*.npy (dataset de reentrenamiento - muy pesado)
- .venv/ (entorno virtual)
- __pycache__/ (cache de Python)

**Tamaños aproximados:**
- data/: ~200-300 MB
- models/: ~50-100 MB por modelo
- focus/: ~200 MB

---

## 🔧 COMANDOS ÚTILES

### Ver paquetes instalados
```powershell
.\.venv\Scripts\Activate.ps1
pip list
```

### Actualizar dependencias
```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Limpiar archivos generados
```powershell
# Limpiar datos (conserva estructura)
Remove-Item data\*.npz, data\*.csv -ErrorAction SilentlyContinue

# Limpiar modelos
Remove-Item models\*.joblib -ErrorAction SilentlyContinue

# Limpiar focus
Remove-Item focus\*.npy -ErrorAction SilentlyContinue
```

---

## 🎯 EJEMPLO DE USO COMPLETO

```powershell
# 1. Iniciar Jupyter
.\start_jupyter.bat

# 2. En Jupyter:
#    - Abrir 01_preparacion_dataset.ipynb
#    - Cell → Run All
#    - Esperar completar (~2 min)

# 3. Abrir 02_modelado_entrenamiento_cmm.ipynb
#    - Cell → Run All
#    - Esperar completar (~20 min)
#    - Verificar: accuracy >80%

# 4. Copiar imágenes de prueba
#    - Pegar JPG/PNG en data/test_images/

# 5. Abrir 03_pruebas_y_predicciones.ipynb
#    - Ejecutar celda de predicciones
#    - Ver resultados

# 6. Si hay clases con <75% accuracy:
#    - Ajustar: CLASSES_TO_RETRAIN = [3, 5]
#    - Ejecutar celda de reentrenamiento
#    - Verificar mejoras
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Jupyter no inicia
```powershell
.\.venv\Scripts\Activate.ps1
jupyter notebook --ip=127.0.0.1 --port=8888
```

### Error de importación
```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Memoria insuficiente
- Reduce batch_size en el cuaderno 02
- Cierra otras aplicaciones

---

## 📊 ESTADO ACTUAL

```
✅ Python 3.10.0 instalado
✅ Entorno virtual creado
✅ 133 paquetes instalados
✅ TensorFlow 2.20.0
✅ Scikit-learn 1.7.2
✅ Numpy 2.2.6
✅ Pandas 2.3.3
✅ Matplotlib 3.10.0
✅ Seaborn 0.13.2
```

---

**¡Todo listo para empezar! 🎉**

Ejecuta: `start_jupyter.bat` y abre el primer cuaderno.
