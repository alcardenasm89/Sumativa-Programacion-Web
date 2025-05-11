import requests
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def juegos_externos(request):
    try:
        # Intentar obtener de caché primero
        juegos = cache.get('rawg_games')
        if juegos is None:
            url = "https://api.rawg.io/api/games"
            params = {
                "key": settings.RAWG_API_KEY,
                "page_size": 12,  # Aumentamos el número de juegos
                "ordering": "-rating",  # Ordenamos por rating
                "metacritic": "80,100"  # Solo juegos con buena calificación
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            juegos = data.get("results", [])
            # Guardar en caché por 1 hora
            cache.set('rawg_games', juegos, 3600)
        
        return render(request, "tienda/juegos_externos.html", {
            "juegos": juegos,
            "title": "Juegos Populares",
            "subtitle": "Descubre los juegos más valorados por la comunidad"
        })
    except RequestException as e:
        print(f"Error al obtener juegos: {str(e)}")
        return render(request, "tienda/juegos_externos.html", {
            "juegos": [], 
            "error": "No se pudieron cargar los juegos",
            "title": "Juegos Populares",
            "subtitle": "Descubre los juegos más valorados por la comunidad"
        })

@api_view(['GET'])
def tipo_cambio(request):
    try:
        # Intentar obtener de caché primero
        clp = cache.get('usd_clp_rate')
        if clp is None:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            clp = data["rates"].get("CLP")
            # Guardar en caché por 1 hora
            cache.set('usd_clp_rate', clp, 3600)
        
        return render(request, "tienda/tipo_cambio.html", {"clp": clp})
    except RequestException as e:
        print(f"Error al obtener tipo de cambio: {str(e)}")
        return render(request, "tienda/tipo_cambio.html", {"clp": None, "error": "No se pudo obtener el tipo de cambio"})