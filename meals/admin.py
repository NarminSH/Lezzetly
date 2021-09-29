from django.contrib import admin
from meals.models import Meal, Category, Property, PropertyOption
# Register your models here.

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ( 'title','price','created_at')
    list_filter = ( 'title','price','created_at')
    search_fields = ('title','price','created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ( 'title', 'created_at')
    search_fields = ('title', 'created_at')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ( 'title', 'created_at')
    search_fields = ('title', 'created_at')


@admin.register(PropertyOption)
class PropertyOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ( 'title', 'created_at')
    search_fields = ('title', 'created_at')