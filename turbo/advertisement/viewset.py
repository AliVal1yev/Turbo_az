from rest_framework import viewsets
from .serializers import CarSerializer, CarModelSerializer, CarNameSerializer
from .models import CarAdvertisement, CarModel, CarName
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser

class CarViewset(viewsets.ModelViewSet):
    queryset = CarAdvertisement.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    
class CarModelViewset(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
class CarNameViewset(viewsets.ModelViewSet):
    queryset = CarName.objects.all()
    serializer_class = CarNameSerializer
    pagination_class = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = PageNumberPagination
    parser_classes = [JSONParser, MultiPartParser] 