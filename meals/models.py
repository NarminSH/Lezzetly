from cooks.models import Cook
from django.db import models
from django.db.models.base import Model


class Category(Model):
    # information
    title = models.CharField('Title', max_length=100, db_index=True)
    # image = models.ImageField('Şəkil', blank=True, upload_to='categories_images')
    description = models.CharField(max_length=255, blank=True)
    # slug = models.SlugField('Slug', max_length=110, editable=False, default='', unique = True)
    is_taste = models.BooleanField('Taste', default=False)
    is_time = models.BooleanField('TimeOfDay', default=False)

    # moderations
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    #relation
    # meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_index=True, related_name='ingredients')

    #information
    title = models.CharField(max_length=100)
    is_active = models.BooleanField('is_active', null=True,blank=True, default=True)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MealOption(models.Model):
    #relation
    # meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_index=True, related_name='options')

    #information
    title = models.CharField(max_length=100)
    is_active = models.BooleanField('is_active', null=True,blank=True, default=True)
    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Meal(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, related_name='meals', on_delete=models.CASCADE)
    mealoption = models.ManyToManyField(MealOption, related_name='meals', db_index=True, blank=True)
    category = models.ManyToManyField(Category, related_name='meals', db_index=True,  blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='meals', db_index=True, blank=True)
    #information
    image = models.ImageField(upload_to='meal_images/')
    title = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2) 
    stock_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    # is_available = models.BooleanField()
    is_active = models.BooleanField(default=True)
    preparing_time = models.CharField(max_length=20)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

