from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    TYPE_CHOICES = [
        ('1', 'Cook'),
        ('2', 'Supplier')
    ]
    patronymic = models.CharField(max_length=60)
    
    # fuad / asagida unique=True -ni sildim
    phone = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='3')
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):   
        return self.first_name

    # fuad / asagidakilari comment-e aldim
    






