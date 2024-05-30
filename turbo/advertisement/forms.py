from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'name', 'model', 'price', 'color', 'year', 'city',
            'category', 'fuel_type', 'engine', 'mileage', 'image',
            'description', 'your_name', 'phone_number', 'your_email','rear_view',
            'hatch', 'parking_radar', 'abs'
        ]
