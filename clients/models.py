from users.models import User
from django.db import models

# Create your models here.

class Client(User):
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)


class Location(models.Model):
    #relation
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_index=True, related_name='locations')

    #information
    address_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)