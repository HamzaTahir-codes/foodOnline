from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register-user/", views.registerUser, name="register-user"),
]
