# Script para configurar entorno virtual de Python
# Ejecutar desde PowerShell: .\setup_venv.ps1

Write-Host "=== Configuración de Entorno Virtual para Django ===" -ForegroundColor Green

# Verificar si Python está instalado
Write-Host "`nVerificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green

# Verificar si pip está instalado
Write-Host "`nVerificando pip..." -ForegroundColor Yellow
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip no está instalado" -ForegroundColor Red
    exit 1
}
Write-Host "pip encontrado: $pipVersion" -ForegroundColor Green

# Crear entorno virtual
Write-Host "`nCreando entorno virtual 'venv'..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "El directorio 'venv' ya existe. ¿Deseas eliminarlo y crear uno nuevo? (S/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "S" -or $response -eq "s") {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "Entorno virtual creado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Usando entorno virtual existente" -ForegroundColor Yellow
    }
} else {
    python -m venv venv
    Write-Host "Entorno virtual creado exitosamente" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "`nInstalando dependencias desde requirements.txt..." -ForegroundColor Yellow
Write-Host "Esto puede tardar varios minutos..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== ¡Configuración completada exitosamente! ===" -ForegroundColor Green
    Write-Host "`nPara activar el entorno virtual en el futuro, ejecuta:" -ForegroundColor Cyan
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "`nPara desactivar el entorno virtual:" -ForegroundColor Cyan
    Write-Host "  deactivate" -ForegroundColor White
} else {
    Write-Host "`nERROR: Hubo problemas instalando las dependencias" -ForegroundColor Red
    Write-Host "Revisa los mensajes de error arriba" -ForegroundColor Yellow
    exit 1
}
