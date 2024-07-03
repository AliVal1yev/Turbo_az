from django import forms
from .models import CarAdvertisement, CarImage
from django.forms import modelformset_factory


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