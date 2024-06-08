from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView

from .forms import CarForm, CarOwnerSignupForm, CarRentForm
from django.contrib.auth.decorators import login_required

from .models import CarOwner, Car, Rental


# Create your views here.
def index(request):
    cars = Car.objects.filter(is_available=True)[:5]  # Get first 5 available cars
    context = {'cars': cars}
    return render(request, 'index.html', context)


@login_required()
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            try:
                car_owner = CarOwner.objects.get(user=request.user)
            except CarOwner.DoesNotExist:
                return redirect('profile')  # TODO: Change url to appropriate one
            car.owner = car_owner
            car.save()
            return redirect('profile')  # TODO: Change url to user home page
    else:
        form = CarForm()
    return render(request, 'create_car_form.html', {'form': form})


@login_required()
def signup_lister(request):
    if request.method == 'POST':
        form = CarOwnerSignupForm(request.POST)
        if form.is_valid():
            car_owner = form.save(commit=False)
            car_owner.user = request.user
            car_owner.save()
            return redirect('/')  # TODO: Change url to user home page
    else:
        form = CarOwnerSignupForm()
    return render(request, 'car_owner_sign_up_form.html', {'form': form})


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    context = {'car': car}
    return render(request, 'car_detail.html', context)


@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    # Check if the user is the owner
    if car.owner.user != request.user:
        return redirect('car_list')  # Or display an error

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            # Handle the image field separately
            if 'image' not in request.FILES:
                form.cleaned_data.pop('image')  # Remove the image field from data

            car = form.save(commit=False)  # Don't save immediately

            if 'image' in request.FILES:
                car.image = form.cleaned_data['image']  # Update image if provided

            car.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request, 'edit_car.html', {'form': form, 'car': car})


# @login_required
# def delete_car(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#
#     # Check if the logged-in user is the owner of the car
#     if car.owner.user != request.user:
#         return redirect('/')  # Or display an error message
#
#     if request.method == 'POST':
#         print(car)
#         car.delete()
#         return redirect('/')
#
#     return redirect('/')
class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('index')  # Replace 'index' with your car list view name

    def test_func(self):
        obj = self.get_object()
        return obj.owner.user == self.request.user

@login_required()
def rent_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == "POST":
        form = CarRentForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.customer = request.user
            rental.save()

            return redirect('profile')
    else:
        form = CarRentForm(initial={'pick_up_date': timezone.now()})

    return render(request, 'rental_form.html', {'form': form, 'car': car})


def rental_confirm(request):
    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')  # Get rental ID from hidden field

        rental = get_object_or_404(Rental, pk=rental_id)

        rental.save()  # Save the rental to the database
        return redirect('/')  # Redirect to success page
    else:
        return redirect('index')  # Handle invalid requests (e.g., GET)

@login_required()
def profile(request):
    user = request.user
    car_owner = CarOwner.objects.filter(user=user).first()

    if request.method == 'POST':
        form = CarOwnerSignupForm(request.POST)
        if form.is_valid():
            car_owner = form.save(commit=False)
            car_owner.user = user
            car_owner.save()
            return redirect('profile')
    else:
        form = CarOwnerSignupForm(initial={'user': user})

    owned_cars = Car.objects.filter(owner=car_owner)
    rented_cars = Car.objects.filter(rental__customer=user)

    return render(request, 'profile.html', {
        'user': user,
        'car_owner': car_owner,
        'owned_cars': owned_cars,
        'rented_cars': rented_cars,
        'form': form
    })
