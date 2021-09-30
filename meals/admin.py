from django.contrib import admin
from meals.models import Meal, Category, Ingredient, MealOption
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


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ( 'title', 'created_at')
    search_fields = ('title', 'created_at')


@admin.register(MealOption)
class PropertyOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ( 'title', 'created_at')
    search_fields = ('title', 'created_at')