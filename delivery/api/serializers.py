from rest_framework import serializers
from delivery.models import Courier, DeliveryArea

class CourierListSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Courier
        fields =(
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'email',
            'transport',
            'work_experience',
            'rating',
            'is_available',
            'latitude',
            'longitude',
        )

