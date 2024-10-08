from django.urls import path
from . import views
from . import viewset



urlpatterns = [
    path(
        'cars/', 
        views.cars, 
        name='cars'
    ),
    path(
        '', 
        views.home, 
        name= 'home'
    ),
    path(
        'about/', 
        views.about, 
        name='about'
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
    
    path(
        'delete_car/<int:id>/',
        views.delete_car,
        name='delete_car'
    ),
    path(
        'login/', 
        views.user_login,
        name='login'
    ),
    path(
        'accounts/login/',
        views.user_login,
        name='login'
    ),
    path(
        'sigup/',
        views.user_signup,
        name='signup'
    ),
    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
    path(
        'mycars/', 
        views.my_cars,
        name='mycars'
    ),
    path(
        'delete_message/<int:id>/', 
        views.delete_car,
        name='delete_message'
    ),
    path(
        'filter/', 
        views.filter_view,
        name='filter'
    ),
    path(
        'toggle-favorite/<int:ad_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
        ),
    path(
        'favorites/',
        views.favorite_cars,
        name='favorite_cars'
    ),
    path(
        'edit_car/<int:ad_id>/',
        views.edit_car,
        name='edit_car'
    ),
    path(
        'verify/',
        views.verify_view,
        name='verify'
    ),
    path(
        'carapi/',
         views.carmodel_view_api,
         name='carapi'
    ),
]

