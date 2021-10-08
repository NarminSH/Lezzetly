from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import os


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):

    TYPE_CHOICES = [
        ('1', 'Cook'),
        ('2', 'Supplier'),
        # ('3', 'Client')
    ]
    patronymic = models.CharField(max_length=60)
    username = None
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
                'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
                },
                settings.SECRET_KEY, algorithm='HS256'
        )
        return token


    def __str__(self):   
        return self.first_name

            
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()






