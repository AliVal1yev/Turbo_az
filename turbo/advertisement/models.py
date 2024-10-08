from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'


class CarName(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'


class CarModel(models.Model):
    name = models.CharField(max_length=32, null=True, blank= True)
    brand = models.ForeignKey(CarName, on_delete=models.CASCADE)
    
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
    PENDING = 'PENDING'
    APPROVE = 'APPROVE'
    REJECTED = 'REJECTED'
    
    CAR_STATUS = {
        APPROVE: 'approve',
        PENDING: 'pending',
        REJECTED: 'rejected'
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank= True)
    name = models.ForeignKey(CarName, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    color = models.CharField(max_length=16)
    year = models.IntegerField(null=True, blank=True)
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
    phone_number = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$', 
                message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed."
            )
        ]
    )
    your_email = models.EmailField(max_length=32)
    car_status = models.CharField(
        max_length=32,
        default=PENDING,
        choices=CAR_STATUS,
        null=True,
        blank=True
        )
    vip_car = models.BooleanField(default=False)
    favorites = models.ManyToManyField(User, related_name='favorites_ads',blank=True)
    watch_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'


class Equipment(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'
    
class CarImage(models.Model):
    car = models.ForeignKey(CarAdvertisement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.car.name} {self.car.model}'
    
    