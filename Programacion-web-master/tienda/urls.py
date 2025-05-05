from django.urls import path
from .api_views import VideojuegoListAPIView, ClienteCreateAPIView
from .external_api_views import juegos_externos, tipo_cambio
from .views import detalle_juego, agregar_comentario

urlpatterns = [
    path('api/videojuegos/', VideojuegoListAPIView.as_view(), name='api-videojuegos'),
    path('api/clientes/', ClienteCreateAPIView.as_view(), name='api-clientes'),
    path('juegos-externos/', juegos_externos, name='juegos-externos'),
    path('tipo-cambio/', tipo_cambio, name='tipo-cambio'),
    path('juego/<int:juego_id>/', detalle_juego, name='detalle-juego'),
    path('juego/<int:juego_id>/comentario/', agregar_comentario, name='agregar-comentario'),
] 