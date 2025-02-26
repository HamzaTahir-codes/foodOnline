from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .context_processors import get_cart_counter, get_cart_amounts
from .models import Cart
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, "marketplace/listings.html", context)

def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # Get the Cart items of the user and pass to the template
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    # For just the categories of the vendor
    # categories = Category.objects.filter(vendor=vendor)
    # For all categories and their related fooditems by using prefetch_related. We are using reverse lookup here.
    categories = Category.objects.prefetch_related(Prefetch('fooditem', queryset = FoodItem.objects.filter(is_available=True))).filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, "marketplace/vendor-details.html", context)

def add_to_cart(request, fooditem_id):
    if request.user.is_authenticated:
        if request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
            #Check if fooditem exists
            try:
                fooditem = FoodItem.objects.get(id=fooditem_id)
                # Check if the user has already added this fooditem to the cart
                try:
                    cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the quantity of the fooditem in the cart
                    cart.quantity += 1
                    cart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased quantity of FoodItem in cart!', 'counter': get_cart_counter(request), 'qty': cart.quantity, 'cart_amounts': get_cart_amounts(request)})
                except:
                    cart = Cart(user=request.user, fooditem=fooditem, quantity=1)
                    cart.save()
                    return JsonResponse({'status': 'Success', 'message': 'FoodItem added to cart!', 'counter': get_cart_counter(request), 'qty': cart.quantity, 'cart_amounts': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'FoodItem does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'User is not Logged In!'})
    
def decrease_qty(request, fooditem_id):
    if request.user.is_authenticated:
        if request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
            #Check if fooditem exists
            try:
                fooditem = FoodItem.objects.get(id=fooditem_id)
                # Check if the user has already added this fooditem to the cart
                try:
                    cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Decrease the quantity of the fooditem in the cart only if there is item greater than 1
                    if cart.quantity > 1:
                        cart.quantity -= 1
                        cart.save()
                    else:
                        cart.delete()
                        cart.quantity = 0
                    return JsonResponse({'status': 'Success', 'message': 'Decreased quantity of FoodItem in cart!', 'counter': get_cart_counter(request), 'qty': cart.quantity, 'cart_amounts': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'FoodItem does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'User is not Logged In!'})

@login_required(login_url='/login/')    
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, "marketplace/cart.html", context)

def delete_cart_item(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(id=item_id)
                cart_item.delete()
                return JsonResponse({'status': 'Success', 'message': 'Cart Item Deleted!', 'counter': get_cart_counter(request),'cart_amounts': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'User is not Logged In!'})

