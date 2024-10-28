from django.core.exceptions import ValidationError
import os

def only_image_validator(value):
    ext = os.path.splitext(value.name)[1] # cover_photo.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported File Extension. Allowed Extensions:'+ str(valid_extensions))