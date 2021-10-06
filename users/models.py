from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import os

class User(AbstractUser):

    TYPE_CHOICES = [
        ('1', 'Cook'),
        ('2', 'Supplier'),
        # ('3', 'Client')
    ]
    patronymic = models.CharField(max_length=60)
    # username = None
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField(('email address'), unique=True, max_length=254)
    phone_regex = RegexValidator(regex = r"^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$", message="Phone number must be entered in the format: '994709616969'. Up to 12 digits")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    user_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='1')

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def token(self):
        token = jwt.encode(
            {
                'username': self.username,
                'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
                },
                os.getenv('SECRET_KEY'), algorithm='HS256'
        )
        return token

    def __str__(self):   
        return self.first_name

    # def save(self):
    #     if self.user_type == '1':
            
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']






