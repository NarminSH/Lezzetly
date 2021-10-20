from django.contrib import admin
from delivery.models import (
    Courier,
    DeliveryArea,
    DeliveryPrice
)

# Register your models here.
@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name','transport','rating','work_experience','is_available','created_at')
    list_filter = ('id', 'first_name','rating','transport','created_at')
    search_fields = ('id','first_name', 'transport')

@admin.register(DeliveryArea)
class DeliveryAreaAdmin(admin.ModelAdmin):
    list_display = (['area_name'])
    list_filter = (['area_name'])
    list_fields = (['area_name'])


admin.site.register(DeliveryPrice)
   


# @admin.register(DeliveryService)
# class DeliveryServiceAdmin(admin.ModelAdmin):
#     list_display = ('cook', 'courier', 'order')
#     list_filter = ('cook', 'courier', 'order')
#     list_fields = ('cook', 'courier', 'order')