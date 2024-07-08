from django import forms
from .models import CarAdvertisement, CarImage, Category, FuelType
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



from django import forms

class CarFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Car Name', max_length=255)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories'
    )
    fuel_type = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        required=False,
        empty_label='All Fuel Type'
    )