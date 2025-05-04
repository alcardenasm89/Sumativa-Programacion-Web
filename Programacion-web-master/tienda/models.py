from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias/')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            while Categoria.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='videojuegos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_lanzamiento = models.DateField()
    desarrollador = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.usuario.username

class Pedido(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Completado'),
        ('A', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.videojuego} x {self.cantidad}"
