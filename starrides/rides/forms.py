from django import forms
from django.core.exceptions import ValidationError

from .models import Car
from .models import CarType
from .models import CarOwner

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'vin', 'car_type', 'transmission', 'mileage', 'doors',
                  'passenger_capacity', 'image', 'is_available']
        widgets = {
            'car_type': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError("This field is required.")

        # File type validation
        if not image.content_type.startswith('image/'):
            raise ValidationError("Upload only image files.")

        # File size validation (in bytes)
        if image.size > 1024 * 1024 * 2:  # 2 MB limit
            raise ValidationError("File size cannot exceed 2 MB.")

        return image


class CarOwnerSignupForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['address', 'phone_number']

