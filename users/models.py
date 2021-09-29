from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    TYPE_CHOICES = [
        ('1', 'Cook'),
        ('2', 'Supplier'),
        ('3', 'Client')
    ]
    patronymic = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    user_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='3')

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):   
        return self.first_name






