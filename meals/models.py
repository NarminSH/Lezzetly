from cooks.models import Cook
from django.db import models
from django.db.models.base import Model

# Create your models here.
class Meal(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, related_name='meals', on_delete=models.CASCADE)

    #information
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2) 
    stock_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    is_active = models.BooleanField()

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    #relation
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_index=True, related_name='properties')

    #information
    name = models.CharField(max_length=100)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PropertyOption(models.Model):
    #relation
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_index=True, related_name='options')
    

