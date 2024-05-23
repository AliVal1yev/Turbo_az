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
    image = models.ImageField(default='fallback.png', blank=True)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'