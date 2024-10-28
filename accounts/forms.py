from django import forms
from .models import User, UserProfile
from .validators import only_image_validator

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number", "password"]

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password Didn't Match!")
        
class UserProfileForm(forms.ModelForm):
    address= forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Start Typing.....", "required":"required"}))
    profile_pictures = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[only_image_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[only_image_validator])
    class Meta:
        model = UserProfile
        fields = ['profile_pictures','cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude'] 

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'longitude' or field == "latitude":
                self.fields[field].widget.attrs['readonly'] = 'readonly'