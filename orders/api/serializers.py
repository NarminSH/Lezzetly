from rest_framework import serializers
from orders.models import Order
from cooks.api.serializers import CookListSerializer

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