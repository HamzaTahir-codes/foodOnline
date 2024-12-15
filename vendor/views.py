from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import detect_vendor_user
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url="accounts:user-login")
@user_passes_test(detect_vendor_user)
def restaurant_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        v_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and v_form.is_valid():
            profile_form.save()
            v_form.save()
            messages.success(request, "Successfully Updated!")
            return redirect('accounts:vendor:restaurant-profile')
        else:
            print("PROFILE ERRORS", profile_form.errors)
            print("VENDOR ERRORS", v_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        v_form = VendorForm(instance=vendor)

    context = {
        "profile_form" : profile_form,
        "v_form" : v_form,
        "profile" : profile,
        "vendor" : vendor,
    }
    return render(request, "vendors/restaurant-profile.html", context)

@login_required(login_url="accounts:user-login")
@user_passes_test(detect_vendor_user)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories' : categories,
    }
    return render(request, 'vendors/menu-builder.html', context)

@login_required(login_url="accounts:user-login")
@user_passes_test(detect_vendor_user)
def food_by_category(request, slug):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, slug=slug)
    fooditems = FoodItem.objects.filter(category=category, vendor=vendor)

    context = {
        "category":category,
        "fooditems":fooditems,
    }
    return render(request, 'vendors/food-by-category.html', context)

'''***CRUD***'''
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Added Successfully!")
            return redirect('accounts:vendor:menu-builder')
        
    else:
        form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "vendors/add-category.html", context)

def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Updated Successfully!")
            return redirect('accounts:vendor:menu-builder')
        
    else:
        form = CategoryForm(instance=category)
    context = {
        "form": form,
        "category" : category,
    }
    return render(request, "vendors/update-category.html", context)

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    messages.success(request, "Category Deleted Successfully!")
    return redirect('accounts:vendor:menu-builder')