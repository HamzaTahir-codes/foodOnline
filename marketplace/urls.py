from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor-details'),

    #Add to Cart
    path('add-to-cart/<int:fooditem_id>/', views.add_to_cart, name='add-to-cart'),
    #Decrease Quantity
    path('decrease-qty/<int:fooditem_id>/', views.decrease_qty, name='decrease-qty'),
    #Delete cart item
    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete-cart-item'),
]