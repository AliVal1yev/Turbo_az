from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from advertisement import views
from advertisement import viewset
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


router = routers.DefaultRouter()
router.register(r'cars', views.CarAdvertisementViewSet)
router.register(r'carnames', views.CarNameViewSet)
router.register(r'carmodels', views.CarModelViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'fueltypes', views.FuelTypeViewSet)
router.register(r'carapi', viewset.CarViewset, basename='carapi')
router.register(r'carmodelapi', viewset.CarModelViewset, basename='carmodelapi')
router.register(r'carnameapi', viewset.CarNameViewset, basename='carnameapi')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('advertisement.urls')), 
    path('api/', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

