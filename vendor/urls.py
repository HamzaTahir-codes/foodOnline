from django.urls import path
from accounts import views as AccountView
from . import views

app_name='vendor'

urlpatterns = [
    path('', AccountView.myAccount),
    path('restaurant-profile/', views.restaurant_profile, name="restaurant-profile"),
    path('menu-builder/', views.menu_builder, name="menu-builder"),

    #Category CRUDS
    path('menu-builder/category/add/', views.add_category, name="add-category"),
    path('menu-builder/category/update/<slug>/', views.update_category, name="update-category"),
    path('menu-builder/category/delete/<slug>/', views.delete_category, name="delete-category"),
    path('menu-builder/category/<slug>/', views.food_by_category, name="food-by-category"),

    #FoodItem CRUDS
    path('menu-builder/food-item/add', views.add_food, name="add-food"),
    path('menu-builder/food-item/update/<slug>/', views.update_food, name="update-food"),
    path('menu-builder/food-item/delete/<slug>/', views.delete_food, name="delete-food"),
]
