from django.contrib import admin
from .models import Categoria, Videojuego, Cliente, Pedido, DetallePedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'stock', 'categoria', 'plataforma')
    list_filter = ('categoria', 'plataforma')
    search_fields = ('titulo', 'desarrollador')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'direccion')
    search_fields = ('usuario__username', 'telefono')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('cliente__usuario__username',)

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'videojuego', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__id', 'videojuego__titulo')
