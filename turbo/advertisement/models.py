from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'


class FuelType(models.Model):
    name =models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'

class City(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self) -> str:
        return f'{self.name}'


class CarAdvertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    price = models.FloatField(null=True)
    color = models.CharField(max_length=16)
    year = models.IntegerField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    engine = models.FloatField(null=True)
    mileage = models.FloatField(null=True)
    description = models.TextField(max_length=3000)
    equipment = models.ManyToManyField('Equipment')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    your_name = models.CharField(max_length=32)
    phone_number = models.IntegerField(null=True)
    your_email = models.EmailField(max_length=32)

    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'


class Equipment(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'
    
class CarImage(models.Model):
    car = models.ForeignKey(CarAdvertisement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True)

    def __str__(self) -> str:
        return f'{self.car.name} {self.car.model}'