from django.http import request
from rest_framework import serializers
from delivery.models import Courier, DeliveryArea, DeliveryPrice

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


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
            # 'deliveryArea',
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
        fields = ('id', 'area_name',)


class DeliveryAreaPriceSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DeliveryPrice
        fields = ('id', 'area', 'delivery_price', 'courier')
        read_only_fields = ['courier']


class DeliveryAreaPriceListSerializer(DeliveryAreaPriceSerializer, DeliveryAreaSerializer):
    area = DeliveryAreaSerializer()



