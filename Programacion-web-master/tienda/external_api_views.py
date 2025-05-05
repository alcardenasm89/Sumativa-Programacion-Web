import requests
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import RequestException

def juegos_externos(request):
    try:
        # Intentar obtener de caché primero
        juegos = cache.get('rawg_games')
        if juegos is None:
            url = "https://api.rawg.io/api/games"
            params = {
                "key": settings.RAWG_API_KEY,
                "page_size": 5
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            juegos = data.get("results", [])
            # Guardar en caché por 1 hora
            cache.set('rawg_games', juegos, 3600)
        
        return render(request, "tienda/juegos_externos.html", {"juegos": juegos})
    except RequestException as e:
        print(f"Error al obtener juegos: {str(e)}")
        return render(request, "tienda/juegos_externos.html", {"juegos": [], "error": "No se pudieron cargar los juegos"})

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