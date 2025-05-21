from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("soundcloud/login/", views.soundcloud_login, name="soundcloud_login"),
    path("soundcloud/callback/", views.soundcloud_callback, name="soundcloud_callback"),
    path("search/", views.search_tracks, name="search_tracks"),
]
