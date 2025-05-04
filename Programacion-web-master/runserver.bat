@echo off
cd /d "%~dp0"
echo Activando entorno virtual...
call "C:\Users\jano_\OneDrive\Documentos\GitHub\Sumativa Programacion Web\.venv\Scripts\activate.bat"
echo Iniciando servidor Django...
python manage.py runserver
pause 