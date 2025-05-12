@echo off
cd /d "%~dp0"

echo Creando entorno virtual...
python -m venv venv

echo Activando entorno virtual...
call "venv\Scripts\activate.bat"

echo Instalando dependencias...
pip install django
pip install django-cors-headers
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install cx_Oracle
pip install Pillow

echo Configuración completada.
echo Ahora puede ejecutar runserver.bat para iniciar el servidor.
pause 