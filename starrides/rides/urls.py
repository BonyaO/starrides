from django.urls import path
from . import views
from .views import CarDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('create_car', views.create_car, name='create_car'),
    path('lister_signup', views.signup_lister, name="Become a Lister"),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='delete_car'),
    path('car/<int:car_id>/rent/', views.rent_car, name='rent_car'),
    path('profile/', views.profile, name='profile')
]