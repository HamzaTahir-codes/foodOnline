from django.urls import path
from accounts import views as AccountView
from . import views

app_name='vendor'

urlpatterns = [
    path('', AccountView.myAccount),
    path('restaurant-profile/', views.restaurant_profile, name="restaurant-profile"),
    path('menu-builder/', views.menu_builder, name="menu-builder"),
    path('menu-builder/category/<slug>/', views.food_by_category, name="food-by-category"),

    #Category CRUDS
    path('menu-builder/category/add/', views.add_category, name="add-category"),
    path('menu-builder/category/update/<slug>/', views.update_category, name="update-category"),
    path('menu-builder/category/delete/<slug>/', views.delete_category, name="delete-category"),
]
