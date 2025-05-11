from django.contrib import admin
from .models import Videojuego, Categoria, Comentario, Cliente, Pedido, DetallePedido

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'stock', 'categoria')
    list_filter = ('categoria', 'fecha_lanzamiento')
    search_fields = ('titulo', 'descripcion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'videojuego', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('texto',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_nacimiento')
    search_fields = ('usuario__username', 'telefono')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('cliente__usuario__username',)

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'videojuego', 'cantidad', 'precio_unitario')
    list_filter = ('pedido__estado',)
    search_fields = ('videojuego__titulo',)

# Personalizar el sitio de administración
admin.site.site_header = 'Panel de Administración'
admin.site.site_title = 'Administración de la Tienda'
admin.site.index_title = 'Bienvenido al Panel de Administración'
