from vendor.models import Vendor
from django.conf import settings

def default(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_api_key(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}