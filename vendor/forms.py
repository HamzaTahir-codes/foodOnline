from django import forms
from .models import Vendor
from accounts.validators import only_image_validator

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[only_image_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']