from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Videojuego, Cliente
from .serializers import VideojuegoSerializer, ClienteSerializer

# Endpoint para listar videojuegos
class VideojuegoListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer

# Endpoint para crear clientes
class ClienteCreateAPIView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# Endpoint para obtener detalles de un videojuego
class VideojuegoDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    lookup_field = 'id'

# Endpoint para actualizar un videojuego
class VideojuegoUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    lookup_field = 'id'

# Endpoint para eliminar un videojuego
class VideojuegoDeleteAPIView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    lookup_field = 'id' 