from django.core.validators import RegexValidator
from django.db import models


class Cook(models.Model):
    # information
    patronymic = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)
    email = models.EmailField(('email address'), unique=True, max_length=254, blank=True, null=True)
    phone_regex = RegexValidator(regex = r"^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$", message="Phone number must be entered in the format: '994709616969'. Up to 12 digits")
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)
    user_type = models.CharField(max_length=5, blank=True, null=True)
    birth_place = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    service_place = models.CharField(max_length=255,blank=True, null=True)
    payment_address = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    is_available = models.BooleanField(blank=True, null=True, default=False)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Cook')
    

    def __str__(self):
        return self.first_name


class Resume(models.Model):
    #relation
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE,
                db_index=True, related_name='resumes')
    #information
    description = models.TextField()

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cook.first_name}'s resume, owner id is {self.cook.id}"


class Recommendation(models.Model):
    #relation
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE,
                db_index=True, related_name='recommendations')
    #infromation
    recommended_by = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recommended_by
