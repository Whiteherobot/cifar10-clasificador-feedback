@echo off
REM ====================================================
REM Script de inicio rápido para Jupyter Notebook
REM ====================================================

echo.
echo ========================================
echo   Proyecto ML - CIFAR-10 con CMM
echo   Iniciando Jupyter Notebook...
echo ========================================
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Verificar que el entorno esté activo
echo [OK] Entorno virtual activado

REM Iniciar Jupyter Notebook
echo.
echo Iniciando Jupyter Notebook en el navegador...
echo Presiona Ctrl+C para detener el servidor
echo.

jupyter notebook

pause
