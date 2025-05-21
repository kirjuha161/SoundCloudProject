from django.shortcuts import render, redirect
from django.conf import settings
import requests


def index(request):
    return render(request, "app/index.html")


def soundcloud_login(request):
    auth_url = (
        "https://soundcloud.com/connect"
        f"?client_id={settings.SOUNDCLOUD_CLIENT_ID}"
        f"&redirect_uri={settings.SOUNDCLOUD_REDIRECT_URI}"
        "&response_type=code"
        "&scope=non-expiring"
    )
    return redirect(auth_url)


def soundcloud_callback(request):
    code = request.GET.get("code")
    if not code:
        return render(request, "app/index.html", {"error": "Нет кода авторизации"})
    token_url = "https://api.soundcloud.com/oauth2/token"
    data = {
        "client_id": settings.SOUNDCLOUD_CLIENT_ID,
        "client_secret": settings.SOUNDCLOUD_CLIENT_SECRET,
        "redirect_uri": settings.SOUNDCLOUD_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()

    return render(request, "app/index.html", {"token_data": token_data})


def search_tracks(request):
    query = request.GET.get("q", "")
    tracks = []
    error = None
    if query:
        url = "https://api.soundcloud.com/tracks"
        params = {
            "client_id": settings.SOUNDCLOUD_CLIENT_ID,
            "q": query,
            "limit": 10,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            tracks = response.json()
        else:
            error = f"Ошибка SoundCloud: {response.status_code} — {response.text}"
    return render(
        request, "app/search.html", {"tracks": tracks, "query": query, "error": error}
    )
