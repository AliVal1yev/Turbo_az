from django.urls import path
from . import views


urlpatterns = [
    path(
        'cars/', 
        views.cars, 
        name='cars'
    ),
    path(
        'home/', 
        views.home, 
        name= 'home'
    ),
    path(
        'about/', 
        views.about, 
        name='about'
    ),
    path(
        'contact/', 
        views.contact, 
        name='contact'
    ),
    path(
        'car/<int:id>/', 
        views.car_details, 
        name='details'
    ),
    path(
        'new_ad/', 
        views.add_advertisement, 
        name='new_ad'
    ),
]