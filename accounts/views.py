from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from .forms import RegisterUserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detectUser
from django.core.exceptions import PermissionDenied

#Restrict vendor from accessing the Customer Dashboard
def detect_vendor_user(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

#Return customer from accessing the Vendor Dashboard
def detect_customer_user(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In!")
        return redirect("accounts:my-account")
    
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
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In!")
        return redirect("accounts:my-account")
    
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

def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In!")
        return redirect("accounts:my-account")
    
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in Successfully!")
            return redirect("accounts:my-account")
        else:
            messages.error(request, "Invalid Credentials! Please try Again")
            return redirect("accounts:user-login")
    return render(request, "accounts/login.html")

def user_logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out successfully! Please Login Again!")
    return redirect("accounts:user-login")

@login_required(login_url="accounts:user-login")
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url="accounts:user-login")
@user_passes_test(detect_customer_user)
def custDashboard(request):
    return render(request, "accounts/customer-dashboard.html")

@login_required(login_url="accounts:user-login")
@user_passes_test(detect_vendor_user)
def venDashboard(request):
    return render(request, "accounts/vendor-dashboard.html")
