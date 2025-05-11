import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Pedido, DetallePedido, Videojuego
from django.shortcuts import get_object_or_404
import json

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@require_POST
def create_payment_intent(request):
    try:
        # Obtener datos del carrito
        carrito_data = request.POST.get('carrito_data')
        if not carrito_data:
            return JsonResponse({'error': 'No hay datos del carrito'}, status=400)
        
        carrito = json.loads(carrito_data)
        if not carrito:
            return JsonResponse({'error': 'El carrito está vacío'}, status=400)

        # Calcular el total
        total = sum(item['precio'] * item['cantidad'] for item in carrito)
        
        # Crear el PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Stripe usa centavos
            currency='clp',
            metadata={
                'user_id': request.user.id,
                'carrito': json.dumps(carrito)
            }
        )

        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def confirm_payment(request):
    try:
        # Obtener el PaymentIntent
        payment_intent_id = request.POST.get('payment_intent_id')
        if not payment_intent_id:
            return JsonResponse({'error': 'No se proporcionó el ID del pago'}, status=400)

        # Verificar el estado del pago
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if intent.status != 'succeeded':
            return JsonResponse({'error': 'El pago no fue exitoso'}, status=400)

        # Obtener datos del carrito del metadata
        carrito = json.loads(intent.metadata.get('carrito', '[]'))
        
        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente=request.user.cliente,
            total=sum(item['precio'] * item['cantidad'] for item in carrito),
            estado='completado'
        )

        # Crear los detalles del pedido y actualizar stock
        for item in carrito:
            juego = get_object_or_404(Videojuego, id=item['id'])
            DetallePedido.objects.create(
                pedido=pedido,
                videojuego=juego,
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            )
            # Actualizar stock
            juego.stock -= item['cantidad']
            juego.save()

        return JsonResponse({
            'success': True,
            'pedido_id': pedido.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400) 