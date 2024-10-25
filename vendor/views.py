from django.shortcuts import render

# Create your views here.
def restaurant_profile(request):
    return render(request, "vendors/restaurant-profile.html")