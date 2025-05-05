from rest_framework import generics
from .models import Videojuego, Cliente
from .serializers import VideojuegoSerializer, ClienteSerializer

# Endpoint para listar videojuegos
class VideojuegoListAPIView(generics.ListAPIView):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer

# Endpoint para crear clientes
class ClienteCreateAPIView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 