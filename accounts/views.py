from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterUserForm
from .models import User
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