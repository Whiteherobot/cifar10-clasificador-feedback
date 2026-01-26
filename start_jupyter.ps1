# ====================================================
# Script de inicio rápido para Jupyter Notebook
# ====================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Proyecto ML - CIFAR-10 con CMM" -ForegroundColor Cyan
Write-Host "  Iniciando Jupyter Notebook..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& .\.venv\Scripts\Activate.ps1

# Verificar que el entorno esté activo
Write-Host "[OK] Entorno virtual activado" -ForegroundColor Green

# Iniciar Jupyter Notebook
Write-Host ""
Write-Host "Iniciando Jupyter Notebook en el navegador..." -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

jupyter notebook
