from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_car', views.create_car, name='Create New Car'),
    path('lister_signup', views.signup_lister, name="Become a Lister"),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:car_id>/delete/', views.delete_car, name='car_delete')
]