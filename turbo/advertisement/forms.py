from django import forms
from .models import CarAdvertisement, CarImage
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = CarAdvertisement
        fields = [
            'name', 'model', 'price', 'color', 'year', 'city',
            'category', 'fuel_type', 'engine', 'mileage','equipment',
            'description', 'your_name', 'phone_number', 'your_email', 
        ]


class AdvertisementImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']

AdvertisementImageFormSet = modelformset_factory(CarImage, form=AdvertisementImageForm, extra=3)