# SEVENGAMER - Tienda de Videojuegos

## Descripción
SEVENGAMER es una plataforma web de comercio electrónico especializada en videojuegos. Permite a los usuarios explorar un catálogo de juegos, realizar compras, dejar comentarios y gestionar su carrito de compras.

## Características Principales
- Catálogo de videojuegos con imágenes y detalles
- Sistema de registro y autenticación de usuarios
- Carrito de compras interactivo
- Sistema de comentarios en tiempo real
- Integración con RAWG API para juegos externos
- Conversión de precios usando API de tipo de cambio
- Diseño responsive y moderno
- Gestión de stock en tiempo real

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Navegador web moderno

## Instalación

1. **Clonar el repositorio**
```bash
git clone [URL_DEL_REPOSITORIO]
cd Programacion-web-master
```

2. **Crear y activar entorno virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear un archivo `credenciales.env` en la raíz del proyecto con el siguiente contenido:
```
RAWG_API_KEY=tu_api_key_de_rawg
SECRET_KEY=tu_clave_secreta_de_django
```

5. **Aplicar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

## Ejecución del Proyecto

1. **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

2. **Acceder a la aplicación**
Abrir el navegador y visitar: `http://127.0.0.1:8000/`

## Estructura del Proyecto
```
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
```

## Características Implementadas

### Catálogo de Juegos
- Visualización de juegos con imágenes y detalles
- Filtrado por categorías
- Búsqueda de juegos
- Detalles completos de cada juego

### Sistema de Usuarios
- Registro de nuevos usuarios
- Inicio de sesión
- Perfil de usuario
- Gestión de pedidos

### Carrito de Compras
- Agregar/eliminar productos
- Actualización en tiempo real
- Cálculo de totales
- Gestión de stock

### Comentarios
- Sistema de comentarios en tiempo real
- Autenticación requerida para comentar
- Visualización de comentarios existentes

### APIs Integradas
- RAWG API para juegos externos
- API de tipo de cambio para conversión de precios

## Solución de Problemas Comunes

### Error de Base de Datos
Si aparece el error "no such table":
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error de API Key
Si los juegos externos no se cargan:
1. Verificar que el archivo `credenciales.env` existe
2. Confirmar que la API key de RAWG es válida
3. Reiniciar el servidor

### Problemas con Imágenes
Si las imágenes no se cargan:
1. Verificar que la carpeta `media` existe
2. Confirmar que los permisos son correctos
3. Ejecutar `python manage.py collectstatic`

