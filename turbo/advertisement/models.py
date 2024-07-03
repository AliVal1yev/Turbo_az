from django.db import models

# Create your models here.


class Advertisement(models.Model):
    name = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    price = models.FloatField(null=True)
    color = models.CharField(max_length=16)
    year = models.IntegerField(null=True)
    city = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    fuel_type = models.CharField(max_length=32)
    engine = models.FloatField(null=True)
    mileage = models.FloatField(null=True)
    image = models.ImageField(default='fallback.png', upload_to='media/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=3000)
    rear_view = models.BooleanField(default=False)
    hatch = models.BooleanField(default=False)
    parking_radar = models.BooleanField(default=False)
    abs = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
    your_name = models.CharField(max_length=32)
    phone_number = models.IntegerField(null=True)
    your_email = models.EmailField(max_length=32)

    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'