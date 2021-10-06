from orders.models import Order
from clients.models import Client
from users.models import User
from django.db import models

# Create your models here.

class Courier(User):
# information
    transport = models.CharField(max_length=150, blank=True, null=True)
    work_experience = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    is_available = models.BooleanField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)


    class Meta:
        verbose_name = ('Courier')


    def __str__(self):
        return self.first_name



class DeliveryArea(models.Model):
    # relations
    courier = models.ForeignKey(Courier, db_index=True, on_delete=models.CASCADE, related_name='delivery_areas')    

    # information
    delivery_area = models.CharField(max_length=150, blank=True, null=True)
    delivery_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.delivery_area

class DeliveryService(models.Model):
    cook = models.ForeignKey(Client, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')
    courier = models.ForeignKey(Courier, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')
    order = models.ForeignKey(Order, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')