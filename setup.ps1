# ============================================================================
# Script de Instalación Automática - ML con CIFAR-10 Classification
# ============================================================================
# Para Windows PowerShell
# Ejecutar como: powershell -ExecutionPolicy Bypass -File setup.ps1
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  INSTALACIÓN AUTOMÁTICA - Proyecto ML con CMM y CIFAR-10" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Función para mostrar errores
function Show-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Función para mostrar éxito
function Show-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

# Función para mostrar info
function Show-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

# [1/5] Verificar Python
Write-Host "[1/5] Verificando instalación de Python..." -ForegroundColor Magenta
$pythonCheck = py --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Show-Error "Python no está instalado o no está en PATH"
    Write-Host ""
    Write-Host "Descarga Python 3.10+ desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Asegúrate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para cerrar"
    exit 1
}
Show-Success "$pythonCheck detectado"

# [2/5] Crear Virtual Environment
Write-Host ""
Write-Host "[2/5] Creando Virtual Environment..." -ForegroundColor Magenta
if (Test-Path ".venv") {
    Show-Success ".venv ya existe"
} else {
    py -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Error al crear virtual environment"
        Read-Host "Presiona Enter para cerrar"
        exit 1
    }
    Show-Success "Virtual environment creado"
}

# [3/5] Activar Virtual Environment
Write-Host ""
Write-Host "[3/5] Activando Virtual Environment..." -ForegroundColor Magenta
& ".venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Show-Error "Error al activar virtual environment"
    Read-Host "Presiona Enter para cerrar"
    exit 1
}
Show-Success "Virtual environment activado"

# [4/5] Actualizar pip
Write-Host ""
Write-Host "[4/5] Actualizando pip..." -ForegroundColor Magenta
python -m pip install --upgrade pip *>$null
if ($LASTEXITCODE -eq 0) {
    Show-Success "pip actualizado"
} else {
    Show-Info "Advertencia: pip podría no actualizarse completamente"
}

# [5/5] Instalar requirements
Write-Host ""
Write-Host "[5/5] Instalando dependencias (esto puede tardar 3-5 minutos)..." -ForegroundColor Magenta
Write-Host ""
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Show-Error "Error al instalar dependencias"
    Write-Host "Intenta ejecutar manualmente:" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Presiona Enter para cerrar"
    exit 1
}

Write-Host ""
Show-Success "Todas las dependencias instaladas correctamente"

# EXTRA: Crear carpetas
Write-Host ""
Write-Host "[EXTRA] Preparando estructura de carpetas..." -ForegroundColor Magenta
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" -ErrorAction SilentlyContinue | Out-Null
}
if (-not (Test-Path "data\test_images")) {
    New-Item -ItemType Directory -Path "data\test_images" -ErrorAction SilentlyContinue | Out-Null
}
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" -ErrorAction SilentlyContinue | Out-Null
}
Show-Success "Carpetas creadas: data/, data/test_images/, models/"

# Resumen final
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1. OPCIÓN A - Iniciar Jupyter automáticamente (recomendado):" -ForegroundColor White
Write-Host "      Presiona 's' a continuación" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. OPCIÓN B - Iniciar manualmente más tarde:" -ForegroundColor White
Write-Host "      - Abre PowerShell en esta carpeta" -ForegroundColor Gray
Write-Host "      - Ejecuta: .venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "      - Luego:  jupyter notebook" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

$startJupyter = Read-Host "¿Deseas iniciar Jupyter ahora? (s/n)"

if ($startJupyter -eq "s") {
    Write-Host ""
    Write-Host "Iniciando Jupyter en http://localhost:8888" -ForegroundColor Green
    Write-Host "(Si no abre automáticamente, copia la URL del terminal)" -ForegroundColor Gray
    Write-Host ""
    jupyter notebook
} else {
    Write-Host ""
    Write-Host "Para ejecutar los cuadernos más tarde:" -ForegroundColor Yellow
    Write-Host "  1. Abre PowerShell en esta carpeta" -ForegroundColor Gray
    Write-Host "  2. Ejecuta: .venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "  3. Luego:  jupyter notebook" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Presiona Enter para cerrar"
}
