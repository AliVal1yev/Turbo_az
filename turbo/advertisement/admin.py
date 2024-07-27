from django.contrib import admin
from .models import CarAdvertisement, Category, Equipment, FuelType, CarImage, City, CarName, CarModel
from .tasks import send_update_notification_task




# class CarAdvertisementAdmin(admin.ModelAdmin):
#     list_display = ('name', 'model', 'car_status')

#     def save_model(self, request, obj, form, change):
#         print(f"save_model called for obj_id {obj.id}")
#         if change:
#             old_status = CarAdvertisement.objects.get(pk=obj.pk).car_status if obj.pk else None
#             print(f"Old status: {old_status}, New status: {obj.car_status}")
#             if obj.car_status == "approve":
#                 super().save_model(request, obj, form, change)
#                 print(f"Triggering email for ad_id {obj.id}")
#                 send_update_notification_task.delay(obj.id)
#             else:
#                 super().save_model(request, obj, form, change)
#         else:
#             super().save_model(request, obj, form, change)


admin.site.register(CarAdvertisement)
admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(FuelType)
admin.site.register(CarImage)
admin.site.register(City)
admin.site.register(CarName)
admin.site.register(CarModel)