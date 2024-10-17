from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import RegisterUserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            #**Django Form**

            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "User Registered Successfully!")
            return redirect("accounts:register-user")

            #**Create Objects**
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # phone_number = form.cleaned_data['phone_number']
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
            # user.role = User.CUSTOMER
            # user.save()
            # return redirect("accounts:register-user")
        # else:
        #     print(form.errors)
    else:
        form = RegisterUserForm()
    context = {
        "form" : form,
    }
    return render(request, "accounts/register-user.html", context)

def registerVendor(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = get_object_or_404(UserProfile, user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your Account Has been Registered! Please wait for Approval")
            return redirect("accounts:register-vendor")
        else:
            messages.error(request, "Error!! Please Fill the form Again!")
    else:
        form = RegisterUserForm()
        v_form = VendorForm()
    context = {
        "form" : form,
        "v_form" : v_form,
    }
    return render(request, "accounts/register-vendor.html", context)