from rest_framework import serializers
from .models import Videojuego, Cliente
from django.contrib.auth.models import User

class VideojuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videojuego
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClienteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Cliente
        fields = '__all__' 