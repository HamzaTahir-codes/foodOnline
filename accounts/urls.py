from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register-user/", views.registerUser, name="register-user"),
    path("register-vendor/", views.registerVendor, name="register-vendor"),
    path("login/", views.user_login, name="user-login"),
    path("logout/", views.user_logout, name="user-logout"),
    path("myAccount/", views.myAccount, name="my-account"),
    path("customer-dashboard/", views.custDashboard, name="customer-dashboard"),
    path("vendor-dashboard/", views.venDashboard, name="vendor-dashboard"),

    #email Verification
    path('activate/<uidb64>/<token>/', views.activate_account, name="activate"),

    #Forgot Password Links
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name="reset-password-validate"),
    path('reset-password/', views.reset_password, name="reset-password"),
]
