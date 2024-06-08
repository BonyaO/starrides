from django import forms
from django.core.exceptions import ValidationError

from .models import Car, Rental
from .models import CarType
from .models import CarOwner

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'vin', 'car_type', 'transmission', 'rental_price', 'mileage', 'doors',
                  'passenger_capacity', 'image', 'is_available']
        widgets = {
            'car_type': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError("This field is required.")

        # File type validation
        # if not image.content_type.startswith('image/'):
        #     raise ValidationError("Upload only image files.")

        # File size validation (in bytes)
        if image.size > 1024 * 1024 * 2:  # 2 MB limit
            raise ValidationError("File size cannot exceed 2 MB.")

        return image


class CarOwnerSignupForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['address', 'phone_number']


class CarRentForm(forms.ModelForm):
    rental_amount = forms.DecimalField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Rental
        fields = ['pick_up_location', 'pick_up_date', 'drop_off_date', 'rental_amount']
        widgets = {
            'pick_up_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'drop_off_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
