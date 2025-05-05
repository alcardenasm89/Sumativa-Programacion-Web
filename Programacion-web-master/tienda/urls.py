from django.urls import path
from .api_views import VideojuegoListAPIView, ClienteCreateAPIView

urlpatterns = [
    path('api/videojuegos/', VideojuegoListAPIView.as_view(), name='api-videojuegos'),
    path('api/clientes/', ClienteCreateAPIView.as_view(), name='api-clientes'),
] 