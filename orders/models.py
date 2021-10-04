from clients.models import Client
from django.db import models
from cooks.models import Cook
from meals.models import Meal
# Create your models here.



class Order(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, on_delete=models.CASCADE, related_name='orders')
    # client = models.ForeignKey(Client,db_index=True, on_delete=models.CASCADE, related_name='orders' )
    #information
    STATUS_CHOICES = [
        ('1', 'Order is confirmed by cook'),
        ('2', 'Preparing order'),
        ('3', 'Order is ready'),
        ('4', 'Courier took order'),
        ('5', 'Courier is on the to you'),
        ('6', 'Order is here!'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    complete = models.BooleanField(default=False)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # test comment from fuad ////s
    # def order_total(self):
    
    @property
    def get_order_total(self):
        # check
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    

class OrderItem(models.Model):
    #relation
    meal = models.ForeignKey(Meal, db_index=True, on_delete=models.CASCADE, related_name='ordered_items' )
    order = models.ForeignKey(Order, db_index=True, on_delete=models.CASCADE, related_name='items' )
    quantity = models.PositiveSmallIntegerField(default=1)
    
    @property
    def total_price(self):
        total_price = self.meal.get_price * self.quantity
        return total_price