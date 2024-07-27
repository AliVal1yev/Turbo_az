from rest_framework import serializers # type: ignore
from .models import CarAdvertisement, CarName, CarModel, Category, FuelType


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAdvertisement
        fields = '__all__'


class CarNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarName
        fields = '__all__'
        

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = '__all__'