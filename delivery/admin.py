from django.contrib import admin
from delivery.models import (
    Courier,
    DeliveryArea,
    DeliveryService
)

# Register your models here.
@admin.register(Courier)
class CookAdmin(admin.ModelAdmin):
    list_display = ( 'first_name','last_name','transport','rating','work_experience','is_available','created_at')
    list_filter = ( 'first_name','rating','transport','created_at')
    search_fields = ('first_name', 'transport')

@admin.register(DeliveryArea)
class DeliveryAreaAdmin(admin.ModelAdmin):
    list_display = ('delivery_area', 'delivery_price')
    list_filter = ('delivery_area', 'delivery_price')
    list_fields = ('delivery_area', 'delivery_price')

@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ('cook', 'courier', 'order')
    list_filter = ('cook', 'courier', 'order')
    list_fields = ('cook', 'courier', 'order')