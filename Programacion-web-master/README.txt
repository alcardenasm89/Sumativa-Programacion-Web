IMPORTANTE!!! PUEDE EJECUTAR EL TERMINAL PROFESOR DESDE RUTA NORMAL python manage.py runserver EN EL TERMINAL DJANGO,CASO CONTRARIOPOR SI NO FUNCIONA DESDE runserver.bat DENTRO DE LA CARPETA Programacion-web-master CLAVE DE ADMIN DJANGO //RUTA ADMIN: http://127.0.0.1:8000/admin/

Usuario: ADMIN1 Pass: Oraclecloud123

CLAVE USUARIO RUTA PAGINA http://127.0.0.1:8000/admin Usuario: juanperez Pass: Juan123! DATOS PARA ENTRAR A BD ORACLE DB_ENGINE=django.db.backends.oracle DB_NAME=HCRHYMIXG8SYHHCH_high DB_USER=ADMIN DB_PASSWORD=Oraclecloud123 DB_HOST=HCRHYMIXG8SYHHCH.adb.sa-santiago-1.oraclecloudapps.com DB_PORT=1522 DJANGO_SECRET_KEY=django-insecure-xn8hb+5l@4!u0kp^9l44tyw*(%hcnhk99-ftblq*@!0=2$mk7& TNS_ADMIN=C:\Users\jano_\OneDrive\Documentos\GitHub\Sumativa Programacion Web\Programacion-web-master\wallet

API Keys
RAWG_API_KEY=4abf08392849407a95da984f94198b30

SEVENGAMER - Tienda de Videojuegos
Descripción
SEVENGAMER es una plataforma web de comercio electrónico especializada en videojuegos. Permite a los usuarios explorar un catálogo de juegos, realizar compras, dejar comentarios y gestionar su carrito de compras.

Características Principales
Catálogo de videojuegos con imágenes y detalles
Sistema de registro y autenticación de usuarios
Carrito de compras interactivo
Sistema de comentarios en tiempo real
Integración con RAWG API para juegos externos
Conversión de precios usando API de tipo de cambio
Diseño responsive y moderno
Gestión de stock en tiempo real
Requisitos Previos
Python 3.8 o superior
pip (gestor de paquetes de Python)
Git
Navegador web moderno
Instalación
Clonar el repositorio
git clone https://github.com/alcardenasm89/Sumativa-Programacion-Web.git
cd Sumativa-Programacion-Web/Programacion-web-master
Crear y activar entorno virtual
# Windows
python -m venv venv
.\venv\Scripts\activate


3. **Instalar dependencias**
```bash
pip install -r requirements.txt
Configurar variables de entorno Crear un archivo credenciales.env en la raíz del proyecto con el siguiente contenido:
RAWG_API_KEY=HCRHYMIXG8SYHHCH
SECRET_KEY=django-insecure-5^&*%$#@!1234567890abcdefghijklmnopqrstuvwxyz
Aplicar migraciones
python manage.py makemigrations
python manage.py migrate
Crear superusuario (opcional)
python manage.py createsuperuser
Ejecución del Proyecto
Iniciar el servidor de desarrollo
python manage.py runserver
Acceder a la aplicación Abrir el navegador y visitar: http://127.0.0.1:8000/
Estructura del Proyecto
Programacion-web-master/
├── tienda/                    # Aplicación principal
│   ├── models.py             # Modelos de la base de datos
│   ├── views.py              # Vistas de la aplicación
│   ├── urls.py               # Configuración de URLs
│   └── templates/            # Plantillas HTML
├── static/                    # Archivos estáticos
│   ├── css/                  # Hojas de estilo
│   ├── js/                   # Scripts JavaScript
│   └── media/                # Imágenes y archivos multimedia
├── requirements.txt          # Dependencias del proyecto
└── manage.py                 # Script de gestión de Django
Características Implementadas
Catálogo de Juegos
Visualización de juegos con imágenes y detalles
Filtrado por categorías
Búsqueda de juegos
Detalles completos de cada juego
Sistema de Usuarios
Registro de nuevos usuarios
Inicio de sesión
Perfil de usuario
Gestión de pedidos
Carrito de Compras
Agregar/eliminar productos
Actualización en tiempo real
Cálculo de totales
Gestión de stock
Comentarios
Sistema de comentarios en tiempo real
Autenticación requerida para comentar
Visualización de comentarios existentes
APIs Integradas
RAWG API para juegos externos
API de tipo de cambio para conversión de precios
Solución de Problemas Comunes
Error de Base de Datos
Si aparece el error "no such table":

python manage.py makemigrations
python manage.py migrate
Error de API Key
Si los juegos externos no se cargan:

Verificar que el archivo credenciales.env existe
Confirmar que la API key de RAWG es válida
Reiniciar el servidor
Problemas con Imágenes
Si las imágenes no se cargan:

Verificar que la carpeta media existe
Confirmar que los permisos son correctos
Ejecutar python manage.py collectstatic