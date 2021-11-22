from django.db import models
from cooks.models import Cook, Client
from delivery.models import Courier, DeliveryPrice
from meals.models import Meal
from django.core.validators import RegexValidator
# Create your models here.



class Order(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, on_delete=models.CASCADE, blank=True, null=True, related_name='orders')
    courier = models.ForeignKey(Courier, db_index=True, on_delete=models.CASCADE, blank=True, null=True, related_name='orders')
    delivery_information = models.ForeignKey(DeliveryPrice, db_index=True, on_delete=models.CASCADE, blank=True, null=True, related_name='orders')
    client = models.ForeignKey(Client,db_index=True, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    #information

    # customer info

    # STATUS_CHOICES = [
    #     ('1', 'Order is confirmed by cook'),
    #     ('2', 'Preparing order'),
    #     ('3', 'Order is ready'),
    #     ('4', 'Courier took order'),
    #     ('5', 'Courier is on the way to you'),
    #     ('6', 'Order is here!'),
    # ]

    # about customer
    # customer_first_name = models.CharField('first name', max_length=150)
    # customer_last_name = models.CharField('last name', max_length=150)
    # customer_phone_regex = RegexValidator(regex = r"^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$", message="Phone number must be entered in the format: '994709616969'. Up to 12 digits")
    # customer_phone = models.CharField(validators=[customer_phone_regex], max_length=12)
    # customer_location = models.CharField('location', max_length=150)

    # customer_email = models.EmailField(('email address'), max_length=254) 
    status = models.CharField(max_length=50, default="order was placed", blank=True, null=True)
    courier_status = models.CharField(max_length=50, default="no courier", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    # is_rejected = models.BooleanField(null=True, blank=True, default=False)
    
    reject_reason = models.CharField('reject reason', max_length=250, null=True, blank=True, default=None)
    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # test comment from fuad ////s
    # def order_total(self):
    
    @property
    def order_total(self):
        # check
        orderitems = self.items.all()
        if orderitems:
            total = sum([item.get_total for item in orderitems])
            return total
        else:
            return 0
    
    def __str__(self):
        return f"Order id is {self.id}"

    

class OrderItem(models.Model):
    #relation
    meal = models.ForeignKey(Meal, db_index=True, on_delete=models.CASCADE, related_name='ordered_items' )
    order = models.ForeignKey(Order, db_index=True, on_delete=models.CASCADE, related_name='items' )
    quantity = models.IntegerField(default=1)
    
    @property
    def meal_title(self):
        return self.meal.title

    @property
    def get_total(self):
        total = self.meal.price * self.quantity
        return total

    # @property
    # def total_price(self):
    #     total_price = self.meal.get_price * self.quantity
    #     return total_price

    def __str__(self):
        return f"Order item id is{self.id}"