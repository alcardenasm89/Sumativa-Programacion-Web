from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Videojuego, Cliente, Pedido
from django.utils import timezone

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'precio', 'stock', 'categoria', 'imagen', 'fecha_lanzamiento', 'desarrollador', 'plataforma']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del videojuego',
                'minlength': '3',
                'maxlength': '200'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del videojuego',
                'rows': 4,
                'minlength': '10'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio',
                'step': '0.01',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad en stock',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'fecha_lanzamiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'desarrollador': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del desarrollador',
                'minlength': '2',
                'maxlength': '100'
            }),
            'plataforma': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la plataforma',
                'minlength': '2',
                'maxlength': '50'
            })
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres')
        if len(titulo) > 200:
            raise forms.ValidationError('El título no puede tener más de 200 caracteres')
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres')
        return descripcion

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que 0')
        if precio > 999999.99:
            raise forms.ValidationError('El precio no puede ser mayor a 999,999.99')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        if stock > 9999:
            raise forms.ValidationError('El stock no puede ser mayor a 9999')
        return stock

    def clean_desarrollador(self):
        desarrollador = self.cleaned_data.get('desarrollador')
        if len(desarrollador) < 2:
            raise forms.ValidationError('El nombre del desarrollador debe tener al menos 2 caracteres')
        if len(desarrollador) > 100:
            raise forms.ValidationError('El nombre del desarrollador no puede tener más de 100 caracteres')
        return desarrollador

    def clean_plataforma(self):
        plataforma = self.cleaned_data.get('plataforma')
        if len(plataforma) < 2:
            raise forms.ValidationError('La plataforma debe tener al menos 2 caracteres')
        if len(plataforma) > 50:
            raise forms.ValidationError('La plataforma no puede tener más de 50 caracteres')
        return plataforma

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La imagen no puede ser mayor a 5MB')
            if not imagen.content_type.startswith('image/'):
                raise forms.ValidationError('El archivo debe ser una imagen')
        return imagen

    def clean_fecha_lanzamiento(self):
        fecha = self.cleaned_data.get('fecha_lanzamiento')
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha de lanzamiento no puede ser futura')
        return fecha

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['direccion', 'telefono']
        widgets = {
            'telefono': forms.TextInput(attrs={'pattern': '[0-9]{9}'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números')
        return telefono

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    username = forms.CharField(
        required=True,
        min_length=4,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso')
        if not username.isalnum():
            raise forms.ValidationError('El nombre de usuario solo puede contener letras y números')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo puede contener letras')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo puede contener letras')
        return last_name

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    username = forms.CharField(
        required=True,
        min_length=4,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password1 = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso')
        if not username.isalnum():
            raise forms.ValidationError('El nombre de usuario solo puede contener letras y números')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo puede contener letras')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo puede contener letras')
        return last_name

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        } 