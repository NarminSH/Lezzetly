from clients.models import Client
from django.db import models
from cooks.models import Cook
from meals.models import Meal
from django.core.validators import RegexValidator
# Create your models here.



class Order(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, on_delete=models.CASCADE, related_name='orders')
    # client = models.ForeignKey(Client,db_index=True, on_delete=models.CASCADE, related_name='orders' )
    #information

    # customer info

    STATUS_CHOICES = [
        ('1', 'Order is confirmed by cook'),
        ('2', 'Preparing order'),
        ('3', 'Order is ready'),
        ('4', 'Courier took order'),
        ('5', 'Courier is on the to you'),
        ('6', 'Order is here!'),
    ]

    
    
    # about customer
    customer_first_name = models.CharField('first name', max_length=150)
    customer_last_name = models.CharField('last name', max_length=150)
    customer_phone_regex = RegexValidator(regex = r"^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$", message="Phone number must be entered in the format: '994709616969'. Up to 12 digits")
    customer_phone = models.CharField(validators=[customer_phone_regex], max_length=12)

    email = models.EmailField(('email address'), unique=True, max_length=254) 
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True, null=True)
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