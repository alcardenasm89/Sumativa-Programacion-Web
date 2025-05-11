from django.urls import path
from .api_views import (
    VideojuegoListAPIView,
    ClienteCreateAPIView,
    VideojuegoDetailAPIView,
    VideojuegoUpdateAPIView,
    VideojuegoDeleteAPIView
)
from .external_api_views import juegos_externos, tipo_cambio
from .views import detalle_juego, agregar_comentario
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/videojuegos/', VideojuegoListAPIView.as_view(), name='api-videojuegos'),
    path('api/videojuegos/<int:id>/', VideojuegoDetailAPIView.as_view(), name='api-videojuego-detail'),
    path('api/videojuegos/<int:id>/update/', VideojuegoUpdateAPIView.as_view(), name='api-videojuego-update'),
    path('api/videojuegos/<int:id>/delete/', VideojuegoDeleteAPIView.as_view(), name='api-videojuego-delete'),
    path('api/clientes/', ClienteCreateAPIView.as_view(), name='api-clientes'),
    
    # External API endpoints
    path('juegos-externos/', juegos_externos, name='juegos_externos'),
    path('tipo-cambio/', tipo_cambio, name='tipo-cambio'),
    
    # Páginas principales
    path('', views.index, name='index'),
    path('juegos/', views.juegos, name='juegos'),
    path('juegos/<int:id>/', views.detalle_juego, name='detalle_juego'),
    path('categorias/', views.categorias, name='categorias'),
    path('categoria/<slug:slug>/', views.categoria_detalle, name='categoria_detalle'),
    path('juegos/categoria/<int:id>/', views.juegos_categoria, name='juegos_categoria'),
    
    # Carrito y pedidos
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedido/<int:id>/', views.detalle_pedido, name='detalle_pedido'),
    
    # Autenticación y perfil
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar-perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('pago/', views.pago, name='pago'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    
    # Panel de administración
    path('panel-admin/', views.panel_admin, name='panel-admin'),
    path('panel-usuario/', views.panel_usuario, name='panel-usuario'),
    path('crear-videojuego/', views.crear_videojuego, name='crear-videojuego'),
    path('editar-videojuego/<int:id>/', views.editar_videojuego, name='editar-videojuego'),
    path('eliminar-videojuego/<int:id>/', views.eliminar_videojuego, name='eliminar-videojuego'),
    path('editar-usuario/<int:id>/', views.editar_usuario, name='editar-usuario'),
    path('eliminar-usuario/<int:id>/', views.eliminar_usuario, name='eliminar-usuario'),
    
    # Comentarios
    path('juego/<int:id>/comentar/', views.agregar_comentario, name='agregar_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 