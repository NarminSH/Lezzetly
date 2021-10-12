from rest_framework import serializers
from delivery.models import Courier, DeliveryArea



class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'email',
            'transport',
            'deliveryArea',
            'work_experience',
            'rating',
            'is_available',
            'location',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {'transport': {'required': True}, 'work_experience': {'required': True}, 
                                                                'location': {'required': True}}
            
        read_only_fields = ['rating'] 


class DeliveryAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryArea
        fields = '__all__'




