from django.contrib import admin
from orders.models import Order, OrderItem
# Register your models here.

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    display = ('created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    display = ('created_at')

