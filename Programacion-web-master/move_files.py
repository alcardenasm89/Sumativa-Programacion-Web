import os
import shutil
from pathlib import Path

# Definir rutas base
BASE_DIR = Path('tienda')
STATIC_DIR = BASE_DIR / 'static' / 'tienda'
MEDIA_DIR = BASE_DIR / 'media'

# Crear directorios si no existen
(STATIC_DIR / 'img').mkdir(parents=True, exist_ok=True)
(MEDIA_DIR / 'videojuegos').mkdir(parents=True, exist_ok=True)
(MEDIA_DIR / 'categorias').mkdir(parents=True, exist_ok=True)

# Archivos de UI que deben moverse a static/tienda/img
UI_FILES = [
    'carrito-compras.png',
    'control4.png',
    'lupa.png',
    'check.png',
    'todos.png',
    'fondo-login.png',
    'fondo_formulario.jpg',
    'gamer.webp'
]

# Mover archivos de UI
for file in UI_FILES:
    src = STATIC_DIR / 'media' / file
    dst = STATIC_DIR / 'img' / file
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f'Movido {file} a static/tienda/img/')

# Mover imágenes de videojuegos
videojuegos_dir = STATIC_DIR / 'media' / 'videojuegos'
if videojuegos_dir.exists():
    for file in videojuegos_dir.glob('*'):
        dst = MEDIA_DIR / 'videojuegos' / file.name
        shutil.move(str(file), str(dst))
        print(f'Movido {file.name} a media/videojuegos/')

# Mover imágenes de categorías
categorias_dir = STATIC_DIR / 'media' / 'categorias'
if categorias_dir.exists():
    for file in categorias_dir.glob('*'):
        dst = MEDIA_DIR / 'categorias' / file.name
        shutil.move(str(file), str(dst))
        print(f'Movido {file.name} a media/categorias/')

print('¡Proceso completado!') 