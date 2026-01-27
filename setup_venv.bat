@echo off
REM Script para configurar entorno virtual de Python (Windows CMD)
REM Ejecutar desde CMD: setup_venv.bat

echo === Configuración de Entorno Virtual para Django ===

REM Verificar Python
echo.
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Crear entorno virtual
echo.
echo Creando entorno virtual 'venv'...
if exist venv (
    echo El directorio 'venv' ya existe.
    set /p response="¿Deseas eliminarlo y crear uno nuevo? (S/N): "
    if /i "%response%"=="S" (
        rmdir /s /q venv
        python -m venv venv
        echo Entorno virtual creado exitosamente
    ) else (
        echo Usando entorno virtual existente
    )
) else (
    python -m venv venv
    echo Entorno virtual creado exitosamente
)

REM Activar entorno virtual
echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias desde requirements.txt...
echo Esto puede tardar varios minutos...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Hubo problemas instalando las dependencias
    echo Revisa los mensajes de error arriba
    pause
    exit /b 1
) else (
    echo.
    echo === ¡Configuración completada exitosamente! ===
    echo.
    echo Para activar el entorno virtual en el futuro, ejecuta:
    echo   venv\Scripts\activate.bat
    echo.
    echo Para desactivar el entorno virtual:
    echo   deactivate
)

pause
