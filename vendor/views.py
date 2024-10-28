from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import detect_vendor_user

# Create your views here.
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