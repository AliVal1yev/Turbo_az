from django.db import models

# Create your models here.
class Advertisement(models.Model):
    name = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    price = models.FloatField(null=True)
    city = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    fuel_type = models.CharField(max_length=32)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'