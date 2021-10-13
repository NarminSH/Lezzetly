from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import JSONField
from delivery.api.serializers import CourierSerializer
from meals.api.serializers import MealSerializer
from meals.models import Meal
from orders.models import Order, OrderItem
from cooks.api.serializers import CookListSerializer, CookSerializer

class OrderCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'customer_first_name',
            'customer_last_name',
            'customer_phone',
            'customer_email',
            'customer_location',
            'complete',
            'created_at',
            'updated_at',
        )

# when creating empty order with customer data and complete false
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'cook',
            # 'status',
            'complete',
            'created_at',
            'updated_at',
        )

class OrderListSerializer(OrderSerializer):
    cook = CookListSerializer()

# class MealSerializerForOrderItem(serializers.ModelSerializer):
#     class Meta:
#         model = Meal
#         fields = (
#             'id',
#             'cook',
#         )

# when create OrderItem
class OrderItemCreateSerializer(serializers.ModelSerializer):
    # order = OrderCreatSerializer()
    # meal = MealSerializer()
    class Meta:
        model = OrderItem
        fields = (
            'quantity',
            # 'order',
            'meal',            
        )


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


class OrderFullSerializer(DynamicFieldsModelSerializer):    #this one is changed
    cook = CookSerializer(required=False)
    courier = CourierSerializer(required=False)
    ordered_items = OrderItemCreateSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'customer_first_name',
            'customer_last_name',
            'customer_phone',
            'customer_email',
            'customer_location',
            'cook',
            'complete',
            'cook',
            'courier',
            'ordered_items',
            'created_at',
            'updated_at',   
        )




class OrderUpdateSerializer(serializers.ModelSerializer):
    cook = CookSerializer(required=False)
    # courier = JSONField()
    ordered_items = OrderItemCreateSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'customer_first_name',
            'customer_last_name',
            'customer_phone',
            'customer_email',
            'customer_location',
            'cook',
            'complete',
            'cook',
            'courier',
            'ordered_items',
            'created_at',
            'updated_at',   
        )