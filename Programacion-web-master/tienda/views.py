from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Videojuego, Categoria
from django.core.files import File
import os
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from tienda.models import Cliente
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Tasa de conversión USD a CLP (aproximada)
TASA_CAMBIO = 1000

# Create your views here.

def index(request):
    titulos = [
        "Resident Evil Village",
        "GTA V",
        "The Witcher 3",
        "FIFA 24",
        "Forza Horizon 5",
        "Final Fantasy XVI",
    ]
    juegos = list(Videojuego.objects.filter(titulo__in=titulos))
    # Ordenar según la lista de títulos
    juegos = sorted(juegos, key=lambda j: titulos.index(j.titulo))
    categorias = Categoria.objects.all()
    return render(request, 'tienda/index.html', {'juegos': juegos, 'categorias': categorias})

def categoria_detalle(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    juegos = Videojuego.objects.filter(categoria=categoria)
    q = request.GET.get('q')
    if q:
        juegos = juegos.filter(titulo__icontains=q)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categoria.html', {
        'categoria': categoria,
        'categorias': categorias,
        'juegos': juegos
    })

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'tienda/login.html', {'error': error})

def registro(request):
    error = None
    success = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmarPassword')
        fecha_nacimiento = request.POST.get('fechaNacimiento')
        direccion = request.POST.get('direccion')
        # Validaciones básicas
        if not all([nombre, username, email, password, confirmar, fecha_nacimiento]):
            error = 'Por favor, completa todos los campos obligatorios.'
        elif password != confirmar:
            error = 'Las contraseñas no coinciden.'
        elif User.objects.filter(username=username).exists():
            error = 'El nombre de usuario ya está en uso.'
        elif User.objects.filter(email=email).exists():
            error = 'El correo electrónico ya está registrado.'
        else:
            try:
                # Validación explícita de contraseña segura
                try:
                    validate_password(password)
                except ValidationError as e:
                    error = e.messages
                    return render(request, 'tienda/registro.html', {'error': error, 'success': success})
                user = User.objects.create_user(username=username, email=email, password=password, first_name=nombre)
                Cliente.objects.create(usuario=user, direccion=direccion or '', fecha_nacimiento=fecha_nacimiento, telefono='')
                success = '¡Registro exitoso! Ahora puedes iniciar sesión.'
            except IntegrityError:
                error = 'Ocurrió un error al registrar el usuario.'
    return render(request, 'tienda/registro.html', {'error': error, 'success': success})

def es_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

def es_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Cliente').exists()

@user_passes_test(es_admin)
def panel_admin(request):
    return render(request, 'tienda/panel-admin.html')

@user_passes_test(es_cliente)
def panel_usuario(request):
    return render(request, 'tienda/panel-usuario.html')

@user_passes_test(es_cliente)
def pago(request):
    return render(request, 'tienda/pago.html')

def recuperar_password(request):
    return render(request, 'tienda/recuperar-password.html')
