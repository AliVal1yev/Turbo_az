from django import forms
from .models import CarAdvertisement, CarImage, Category, FuelType, CarName, CarModel
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6)



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


AdvertisementImageFormSet = forms.inlineformset_factory(
    CarAdvertisement,
    CarImage,
    form=AdvertisementImageForm,
    extra=2,
    can_delete=True,
)

class CarFilterForm(forms.Form):
    car_brand = forms.ModelChoiceField(
        queryset=CarName.objects.all(),
        required=False,
        empty_label='All Brands'
    )
    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        empty_label='All Models'
    )
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