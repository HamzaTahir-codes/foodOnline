from .models import Cart
from menu.models import FoodItem

def get_cart_counter(request):
    # Get the cart count for the user
    cart_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the cart items for the user
        try:
            cart_items = Cart.objects.filter(user=request.user)
            # Calculate the cart count
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(id=item.fooditem.id)
            subtotal += fooditem.price * item.quantity
        grand_total += subtotal + tax
    return {'subtotal': subtotal, 'tax': tax, 'grand_total': grand_total}