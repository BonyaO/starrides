from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator

class CarType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CarOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.last_name

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=50, unique=True)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    transmission = models.CharField(max_length=10)
    mileage = models.IntegerField()
    doors = models.IntegerField()
    passenger_capacity = models.IntegerField()
    image = models.ImageField(upload_to='car_images/')  # Adjust upload path as needed
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pick_up_location = models.CharField(max_length=255)
    pick_up_date = models.DateTimeField()
    drop_off_date = models.DateTimeField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"Rental ID: {self.id} - Car: {self.car}"




