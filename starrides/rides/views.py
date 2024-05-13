from django.shortcuts import render, redirect, get_object_or_404
from .forms import CarForm, CarOwnerSignupForm
from django.contrib.auth.decorators import login_required

from .models import CarOwner, Car


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
                return redirect('/')    # TODO: Change url to appropriate one
            car.owner = car_owner
            car.save()
            return redirect('/')    # TODO: Change url to user home page
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

    # Check if the logged-in user is the owner of the car
    if car.owner.user != request.user:
        return redirect('car_list')  # Or display an error message

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)  # Redirect to car details
    else:
        form = CarForm(instance=car)

    return render(request, 'car_edit.html', {'form': form, 'car': car})


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    # Check if the logged-in user is the owner of the car
    if car.owner.user != request.user:
        return redirect('/')  # Or display an error message

    if request.method == 'POST':
        car.delete()
        return redirect('/')

    return redirect('/')
