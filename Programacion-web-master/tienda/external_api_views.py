import requests
from django.shortcuts import render

def juegos_externos(request):
    url = "https://api.rawg.io/api/games"
    params = {
        "key": "YOUR_RAWG_API_KEY",  # Reemplaza con tu API KEY de RAWG
        "page_size": 5
    }
    response = requests.get(url, params=params)
    juegos = response.json().get("results", [])
    return render(request, "tienda/juegos_externos.html", {"juegos": juegos})

def tipo_cambio(request):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    clp = data["rates"].get("CLP")
    return render(request, "tienda/tipo_cambio.html", {"clp": clp}) 