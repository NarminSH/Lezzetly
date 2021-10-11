from django.db.models import fields
from rest_framework import serializers
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
            'status',
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

class OrderFullSerializer(serializers.ModelSerializer):
    cook = CookSerializer(required=False)
    ordered_items = OrderItemCreateSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'customer_first_name',
            'customer_last_name',
            'customer_phone',
            'customer_email',
            'cook',
            'complete',
            'cook',
            'ordered_items',
            'created_at',
            'updated_at',   
        )