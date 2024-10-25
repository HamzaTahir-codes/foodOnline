from django.urls import path
from accounts import views as AccountView
from . import views

app_name='vendor'

urlpatterns = [
    path('', AccountView.myAccount),
    path('restaurant-profile/', views.restaurant_profile, name="restaurant-profile"),
]
