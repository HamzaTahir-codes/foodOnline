from django import forms
from .models import Category, FoodItem
from accounts.validators import only_image_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[only_image_validator])
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']