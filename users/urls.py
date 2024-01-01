from django.urls import path

from .views import *

app_name = "users"
urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("ban", ban, name="ban")
]
