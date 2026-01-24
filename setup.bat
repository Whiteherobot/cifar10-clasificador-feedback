@echo off
REM ============================================================================
REM Script de Instalación Automática - ML con CIFAR-10 Classification
REM ============================================================================
REM Este script configura automáticamente el entorno para ejecutar los cuadernos
REM ============================================================================

setlocal enabledelayedexpansion
title Configuración del Proyecto ML - CIFAR-10

echo.
echo ============================================================================
echo   INSTALACIÓN AUTOMÁTICA - Proyecto ML con CMM y CIFAR-10
echo ============================================================================
echo.

REM Verificar si Python está instalado
echo [1/5] Verificando instalación de Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo Descarga Python 3.10+ desde: https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('py --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% detectado

REM Crear Virtual Environment
echo.
echo [2/5] Creando Virtual Environment...
if exist .venv (
    echo ✅ .venv ya existe
) else (
    py -m venv .venv
    if errorlevel 1 (
        echo ❌ Error al crear virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment creado
)

REM Activar Virtual Environment
echo.
echo [3/5] Activando Virtual Environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activado

REM Actualizar pip
echo.
echo [4/5] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Advertencia: pip podría no actualizarse completamente
) else (
    echo ✅ pip actualizado
)

REM Instalar requirements
echo.
echo [5/5] Instalando dependencias (esto puede tardar 3-5 minutos)...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Error al instalar dependencias
    echo Intenta ejecutar manualmente:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo.
echo ✅ Todas las dependencias instaladas correctamente

REM Crear carpeta data si no existe
echo.
echo [EXTRA] Preparando estructura de carpetas...
if not exist data mkdir data
if not exist data\test_images mkdir data\test_images
if not exist models mkdir models
echo ✅ Carpetas creadas: data/, data/test_images/, models/

REM Resumen final
echo.
echo ============================================================================
echo   ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================================
echo.
echo 📋 Próximos pasos:
echo.
echo   1. OPCIÓN A - Iniciar Jupyter automáticamente (recomendado):
echo      Presiona Enter a continuación
echo.
echo   2. OPCIÓN B - Iniciar manualmente más tarde:
echo      - Abre terminal en esta carpeta
echo      - Ejecuta: .venv\Scripts\activate
echo      - Luego:  jupyter notebook
echo.
echo ============================================================================
echo.

REM Preguntar si desea iniciar Jupyter
set /p START_JUPYTER="¿Deseas iniciar Jupyter ahora? (s/n): "

if /i "%START_JUPYTER%"=="s" (
    echo.
    echo Iniciando Jupyter en http://localhost:8888
    echo (Si no abre automáticamente, copia la URL del terminal)
    echo.
    jupyter notebook
) else (
    echo.
    echo Para ejecutar los cuadernos más tarde:
    echo   1. Abre PowerShell o Cmd en esta carpeta
    echo   2. Ejecuta: .venv\Scripts\activate
    echo   3. Luego:  jupyter notebook
    echo.
    pause
)

endlocal
