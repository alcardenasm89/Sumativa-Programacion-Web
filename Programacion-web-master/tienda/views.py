from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Videojuego, Categoria, Comentario, Cliente, Pedido, DetallePedido
from django.core.files import File
import os
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from tienda.models import Cliente
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import VideojuegoForm, ClienteForm, UserForm, UserRegistrationForm
from django.db.models import Q
import json
from django.urls import reverse
from django.db import models
import stripe
from django.conf import settings
import requests
from django.core.cache import cache

# Tasa de conversión USD a CLP (aproximada)
TASA_CAMBIO = 1000

# Create your views here.

def index(request):
    juegos = Videojuego.objects.all()[:6]  # Mostrar solo los 6 juegos más recientes
    categorias = Categoria.objects.all()
    
    # Obtener juegos externos
    try:
        juegos_externos = cache.get('rawg_games')
        if juegos_externos is None:
            url = "https://api.rawg.io/api/games"
            params = {
                "key": settings.RAWG_API_KEY,
                "page_size": 6,  # Mostrar solo 6 juegos en la página principal
                "ordering": "-rating",
                "metacritic": "80,100"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            juegos_externos = data.get("results", [])
            cache.set('rawg_games', juegos_externos, 3600)
    except Exception as e:
        print(f"Error al obtener juegos externos: {str(e)}")
        juegos_externos = []
    
    return render(request, 'tienda/index.html', {
        'juegos': juegos,
        'categorias': categorias,
        'juegos_externos': juegos_externos
    })

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

def juegos(request):
    juegos = Videojuego.objects.all()
    categorias = Categoria.objects.all()  # Agregamos las categorías al contexto
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        juegos = juegos.filter(titulo__icontains=query)
    
    return render(request, 'tienda/juegos.html', {
        'juegos': juegos,
        'categorias': categorias,  # Incluimos las categorías en el contexto
    })

def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categorias.html', {'categorias': categorias})

def juegos_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    juegos = Videojuego.objects.filter(categoria=categoria)
    categorias = Categoria.objects.all()  # Agregamos las categorías al contexto
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        juegos = juegos.filter(titulo__icontains=query)
    
    return render(request, 'tienda/categoria.html', {
        'categoria': categoria,
        'juegos': juegos,
        'categorias': categorias,  # Incluimos las categorías en el contexto
    })

def carrito(request):
    if not request.session.get('carrito'):
        request.session['carrito'] = {}
    carrito = request.session['carrito']
    juegos = []
    total = 0
    for id, cantidad in carrito.items():
        juego = get_object_or_404(Videojuego, id=id)
        subtotal = juego.precio * cantidad
        juegos.append({
            'juego': juego,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        total += subtotal
    return render(request, 'tienda/carrito.html', {
        'juegos': juegos,
        'total': total
    })

@require_POST
def agregar_al_carrito(request, id):
    if not request.session.get('carrito'):
        request.session['carrito'] = {}
    carrito = request.session['carrito']
    cantidad = int(request.POST.get('cantidad', 1))
    if id in carrito:
        carrito[id] += cantidad
    else:
        carrito[id] = cantidad
    request.session['carrito'] = carrito
    return redirect('carrito')

@require_POST
def eliminar_del_carrito(request, id):
    if request.session.get('carrito'):
        carrito = request.session['carrito']
        if str(id) in carrito:
            del carrito[str(id)]
            request.session['carrito'] = carrito
    return redirect('carrito')

@require_POST
def actualizar_carrito(request, id):
    if request.session.get('carrito'):
        carrito = request.session['carrito']
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad > 0:
            carrito[str(id)] = cantidad
        else:
            del carrito[str(id)]
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def checkout(request):
    # Verificar si el usuario tiene un perfil de cliente completo
    try:
        cliente = Cliente.objects.get(usuario=request.user)
        if not cliente.direccion or not cliente.telefono:
            messages.warning(request, 'Por favor, completa tu perfil con dirección y teléfono antes de realizar una compra.')
            return redirect('editar-perfil')
    except Cliente.DoesNotExist:
        messages.warning(request, 'Por favor, completa tu perfil antes de realizar una compra.')
        return redirect('editar-perfil')

    if request.method == 'POST':
        # Obtener datos del carrito del localStorage
        carrito_data = request.POST.get('carrito_data')
        if not carrito_data:
            messages.error(request, 'No hay items en el carrito')
            return redirect('carrito')
        
        try:
            carrito = json.loads(carrito_data)
            if not carrito:
                messages.error(request, 'No hay items en el carrito')
                return redirect('carrito')

            # Validar stock antes de crear la orden
            for item in carrito:
                try:
                    juego = Videojuego.objects.get(id=item['id'])
                    if juego.stock < item['cantidad']:
                        messages.error(request, f'Stock insuficiente para {juego.titulo}. Disponible: {juego.stock}')
                        return redirect('carrito')
                except Videojuego.DoesNotExist:
                    messages.error(request, f'El juego con ID {item["id"]} no existe')
                    return redirect('carrito')

            # Crear el PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(sum(item['precio'] * item['cantidad'] for item in carrito) * 100),
                currency='clp',
                metadata={
                    'user_id': request.user.id,
                    'carrito': carrito_data
                }
            )

            return JsonResponse({
                'status': 'success',
                'clientSecret': intent.client_secret
            })
            
        except json.JSONDecodeError:
            messages.error(request, 'Error al procesar el carrito')
            return redirect('carrito')
        except Exception as e:
            messages.error(request, f'Error al procesar la orden: {str(e)}')
            return redirect('carrito')

    # GET request - mostrar el formulario de checkout
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('carrito')

    juegos = []
    total = 0
    for id, cantidad in carrito.items():
        try:
            juego = get_object_or_404(Videojuego, id=id)
            subtotal = juego.precio * cantidad
            juegos.append({
                'juego': juego,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Videojuego.DoesNotExist:
            messages.error(request, f'El juego con ID {id} no existe')
            continue

    if not juegos:
        messages.error(request, 'No hay juegos válidos en el carrito')
        return redirect('carrito')

    return render(request, 'tienda/checkout.html', {
        'juegos': juegos,
        'total': total,
        'cliente': cliente,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def pedidos(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha_pedido')
    except Cliente.DoesNotExist:
        pedidos = []
    
    return render(request, 'tienda/pedidos.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, id):
    # Aquí iría la lógica para mostrar el detalle de un pedido
    return render(request, 'tienda/detalle_pedido.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Si es superusuario, redirigir al panel de Django admin
            if user.is_superuser:
                return redirect('/admin/')
            # Si es staff pero no superusuario, redirigir al panel de tienda
            elif user.is_staff:
                return redirect('panel-admin')
            # Si es usuario normal
            else:
                return redirect('panel-usuario')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'tienda/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Cliente.objects.create(usuario=user)
                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'tienda/registro.html', {'form': form})

def es_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

def es_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Cliente').exists()

def is_admin(user):
    return user.is_staff

# Admin Panel Views
@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_admin(request):
    videojuegos = Videojuego.objects.all().order_by('-id')
    usuarios = User.objects.all().order_by('-id')
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    return render(request, 'tienda/panel-admin.html', {
        'videojuegos': videojuegos,
        'usuarios': usuarios,
        'pedidos': pedidos
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                videojuego = form.save()
                messages.success(request, f'Videojuego "{videojuego.titulo}" creado exitosamente.')
                return redirect('panel-admin')
            except Exception as e:
                messages.error(request, f'Error al crear el videojuego: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = VideojuegoForm()
    return render(request, 'tienda/editar-videojuego.html', {
        'form': form,
        'titulo': 'Crear Videojuego'
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_videojuego(request, id):
    videojuego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=videojuego)
        if form.is_valid():
            try:
                videojuego = form.save()
                messages.success(request, f'Videojuego "{videojuego.titulo}" actualizado exitosamente.')
                return redirect('panel-admin')
            except Exception as e:
                messages.error(request, f'Error al actualizar el videojuego: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = VideojuegoForm(instance=videojuego)
    return render(request, 'tienda/editar-videojuego.html', {
        'form': form,
        'titulo': 'Editar Videojuego',
        'videojuego': videojuego
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_videojuego(request, id):
    videojuego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        videojuego.delete()
        messages.success(request, 'Videojuego eliminado exitosamente.')
        return redirect('panel-admin')
    return render(request, 'tienda/eliminar-videojuego.html', {
        'videojuego': videojuego
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('panel-admin')
    else:
        form = UserForm(instance=usuario)
    return render(request, 'tienda/editar-usuario.html', {
        'form': form,
        'usuario': usuario,
        'titulo': 'Editar Usuario'
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('panel-admin')
    return render(request, 'tienda/eliminar-usuario.html', {
        'usuario': usuario
    })

# User Panel Views
@login_required
def panel_usuario(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha_creacion')
        
        # Estadísticas del usuario
        total_pedidos = pedidos.count()
        pedidos_pendientes = pedidos.filter(estado='pendiente').count()
        pedidos_completados = pedidos.filter(estado='completado').count()
        total_gastado = sum(pedido.total for pedido in pedidos.filter(estado='completado'))
        
        # Pedidos recientes (últimos 5)
        pedidos_recientes = pedidos[:5]
        
        # Juegos más comprados
        juegos_mas_comprados = Videojuego.objects.filter(
            detallepedido__pedido__cliente=cliente
        ).annotate(
            total_compras=models.Count('detallepedido')
        ).order_by('-total_compras')[:5]
        
        # Categorías favoritas
        categorias_favoritas = Categoria.objects.filter(
            videojuego__detallepedido__pedido__cliente=cliente
        ).annotate(
            total_compras=models.Count('videojuego__detallepedido')
        ).order_by('-total_compras')[:5]
        
    except Cliente.DoesNotExist:
        cliente = None
        pedidos = []
        total_pedidos = 0
        pedidos_pendientes = 0
        pedidos_completados = 0
        total_gastado = 0
        pedidos_recientes = []
        juegos_mas_comprados = []
        categorias_favoritas = []
    
    return render(request, 'tienda/panel-usuario.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_completados': pedidos_completados,
        'total_gastado': total_gastado,
        'pedidos_recientes': pedidos_recientes,
        'juegos_mas_comprados': juegos_mas_comprados,
        'categorias_favoritas': categorias_favoritas
    })

@login_required
def editar_perfil(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        cliente = None

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        cliente_form = ClienteForm(request.POST, instance=cliente) if cliente else None

        if user_form.is_valid():
            try:
                user = user_form.save()
                if cliente_form and cliente_form.is_valid():
                    cliente_form.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('perfil')
            except Exception as e:
                messages.error(request, f'Error al actualizar el perfil: {str(e)}')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            if cliente_form and cliente_form.errors:
                for field, errors in cliente_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        user_form = UserForm(instance=request.user)
        cliente_form = ClienteForm(instance=cliente) if cliente else None

    return render(request, 'tienda/editar-perfil.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'cliente': cliente,
        'titulo': 'Editar Perfil'
    })

@user_passes_test(es_cliente)
def pago(request):
    return render(request, 'tienda/pago.html')

def recuperar_password(request):
    return render(request, 'tienda/recuperar-password.html')

def detalle_juego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    comentarios = Comentario.objects.filter(videojuego=juego).order_by('-fecha_creacion')
    return render(request, 'tienda/detalle_juego.html', {
        'juego': juego,
        'comentarios': comentarios
    })

@login_required
@require_POST
def agregar_comentario(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    texto = request.POST.get('texto')
    if texto:
        Comentario.objects.create(
            usuario=request.user,
            videojuego=juego,
            texto=texto
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'El comentario no puede estar vacío'}, status=400)

@login_required
def perfil(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        cliente = None
    return render(request, 'tienda/perfil.html', {
        'cliente': cliente,
        'user': request.user
    })

@login_required
def payment_success(request):
    payment_intent_id = request.GET.get('payment_intent')
    if not payment_intent_id:
        messages.error(request, 'No se pudo verificar el pago')
        return redirect('carrito')
    
    try:
        # Verificar el estado del pago con Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == 'succeeded':
            # El pago fue exitoso, limpiar el carrito
            if 'carrito' in request.session:
                del request.session['carrito']
            
            messages.success(request, '¡Pago realizado con éxito! Tu pedido ha sido procesado.')
            return redirect('panel_usuario')
        else:
            messages.error(request, 'El pago no se completó correctamente')
            return redirect('carrito')
            
    except Exception as e:
        messages.error(request, f'Error al verificar el pago: {str(e)}')
        return redirect('carrito')

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Verificar que la contraseña actual sea correcta
        if not request.user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta')
            return render(request, 'tienda/cambiar_password.html')
        
        # Verificar que las nuevas contraseñas coincidan
        if new_password != confirm_password:
            messages.error(request, 'Las nuevas contraseñas no coinciden')
            return render(request, 'tienda/cambiar_password.html')
        
        # Validar la nueva contraseña
        try:
            validate_password(new_password, request.user)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'tienda/cambiar_password.html')
        
        # Cambiar la contraseña
        request.user.set_password(new_password)
        request.user.save()
        
        # Actualizar la sesión para evitar que el usuario sea desconectado
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Contraseña actualizada exitosamente')
        return redirect('perfil')
    
    return render(request, 'tienda/cambiar_password.html')
