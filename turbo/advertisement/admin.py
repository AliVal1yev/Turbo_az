from django.contrib import admin
from .models import CarAdvertisement, Category, Equipment, FuelType, CarImage, City, CarName, CarModel


admin.site.register(CarAdvertisement)
admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(FuelType)
admin.site.register(CarImage)
admin.site.register(City)
admin.site.register(CarName)
admin.site.register(CarModel)