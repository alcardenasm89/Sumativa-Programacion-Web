@echo off
cd /d "%~dp0"

echo Verificando entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo Error: No se encontró el entorno virtual.
    echo Por favor, ejecute setup.bat primero.
    pause
    exit /b 1
)

echo Activando entorno virtual...
call "venv\Scripts\activate.bat"

echo Verificando instalación de Django...
python -c "import django" 2>nul
if errorlevel 1 (
    echo Error: Django no está instalado.
    echo Por favor, ejecute setup.bat primero.
    pause
    exit /b 1
)

echo Iniciando servidor Django...
python manage.py runserver
pause 