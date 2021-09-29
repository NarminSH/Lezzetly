from django.contrib import admin
from clients.models import Client, Location
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ( 'first_name','last_name','created_at')
    list_filter = ( 'first_name','last_name','created_at')
    search_fields = ('first_name', 'created_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ( 'address_name','created_at')
    list_filter = ('address_name','created_at')
    search_fields = ('address_name', 'created_at')