from users.models import User
from django.db import models



class Cook(User):
# information
    birth_place = models.CharField(max_length=150)
    city = models.CharField(max_length=150, blank=True, null=True)
    service_place = models.CharField(max_length=255,blank=True, null=True)
    payment_address = models.CharField(max_length=255)
    work_experience = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    is_available = models.BooleanField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)



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
        return self.cook


class Recommendation(models.Model):
    #relation
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE,
                db_index=True, related_name='recommendations')
    #infromation
    recommended_by = models.CharField(max_length=255)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recommended_by
