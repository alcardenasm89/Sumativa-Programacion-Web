from django.shortcuts import redirect
from django.urls import reverse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Panel admin: solo administradores
        if request.path.startswith('/panel-admin') and not (
            request.user.is_authenticated and request.user.groups.filter(name='Administrador').exists()
        ):
            return redirect(reverse('login'))

        # Panel usuario: solo clientes
        if request.path.startswith('/panel-usuario') and not (
            request.user.is_authenticated and request.user.groups.filter(name='Cliente').exists()
        ):
            return redirect(reverse('login'))

        return self.get_response(request) 