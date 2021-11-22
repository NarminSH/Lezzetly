# from orders.models import Order
# from clients.models import Client
from django.core.validators import RegexValidator
# from users.models import User
from django.db import models

# Create your models here.

# class Courier(models.Model):

#     #relations
#     # deliveryArea = models.ManyToManyField(DeliveryArea, related_name='meals', db_index=True)

#     # information
#     patronymic = models.CharField(max_length=60, blank=True, null=True)
#     username = models.CharField(max_length=200, unique=True, blank=True, null=True)
#     first_name = models.CharField('first name', max_length=150, blank=True, null=True)
#     last_name = models.CharField('last name', max_length=150, blank=True, null=True)
#     email = models.EmailField(('email address'), unique=True, max_length=254, blank=True, null=True)
#     phone_regex = RegexValidator(regex = r"^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$", message="Phone number must be entered in the format: '994709616969'. Up to 12 digits")
#     phone = models.CharField(validators=[phone_regex], max_length=12)
#     user_type = models.CharField(max_length=5, blank=True, null=True)
#     transport = models.CharField(max_length=150, blank=True, null=True)
#     work_experience = models.IntegerField(blank=True, null=True)
#     rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
#     is_available = models.BooleanField(blank=True, null=True, default=False)
#     location = models.CharField(max_length=255, blank=True, null=True)


#     # moderations
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         verbose_name = ('Courier')


    # def __str__(self):
    #     return self.username

# it is fake
class Courier(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    usertype = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null=True)
    transport = models.CharField(max_length=150, null=True)
    work_experience = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True) # belke burda digiti 1 ele
    location = models.CharField(max_length=255, null=True)
    is_available = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = False
       db_table = 'couriers'

    def __str__(self):
        return self.username


class DeliveryArea(models.Model):
    area_name = models.CharField(max_length=150)

    def __str__(self):
        return self.area_name


class DeliveryPrice(models.Model):
    area = models.ForeignKey(DeliveryArea, db_index=True, related_name='exact_places', on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, db_index=True, related_name='delivery_areas', on_delete=models.CASCADE, blank=True, null=True)

    delivery_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Price for {self.area.area_name} is {self.delivery_price } ,  for {  self.courier.first_name}"






# class DeliveryPrice(models.Model):
#     # relations
#     # courier = models.ForeignKey(Courier, db_index=True, on_delete=models.CASCADE, related_name='delivery_areas')

#     # information
#     delivery_price = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return f"Price is {self.delivery_price}"







# class DeliveryService(models.Model):
#     cook = models.ForeignKey(Client, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')
#     courier = models.ForeignKey(Courier, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')
#     order = models.ForeignKey(Order, db_index=True, on_delete=models.CASCADE, related_name='delivery_services')

#     def __str__(self):
#         return f"Delivery Service id is{self.id}"