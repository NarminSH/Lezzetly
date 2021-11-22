from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import CharField, JSONField
from delivery.api.serializers import CourierSerializer, DeliveryAreaOrderForAddCourierSerializer, DeliveryAreaOrderSerializer
from meals.api.serializers import MealOrderItemSerializer, MealSerializer
from meals.models import Meal
from orders.models import Order, OrderItem
from cooks.models import Client, Cook
from delivery.models import Courier
from cooks.api.serializers import CookListSerializer, CookSerializer

class OrderCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
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



class OrderForItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        meal = MealOrderItemSerializer(read_only=True, required=False)
        fields = (
            'id',
            'complete',   
        )

class OrderItemForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'quantity',
            'meal',
            'meal_title'
        )

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderForItemSerializer(read_only=True, required=False)
    meal = MealOrderItemSerializer(read_only=True, required=False)
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'quantity',
            'order',
            'meal',
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    cook = CookSerializer(required=False)
    # courier = JSONField()
    items = OrderItemCreateSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'cook',
            'complete',
            'cook',
            'courier',
            'items',
            'created_at',
            'updated_at',   
        )

class CookForOrderSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods
    class Meta:
        model = Cook
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'service_place',  
            'payment_address',
            # 'is_available',
            
        )
        # read_only_fields = ['rating', ]

class CookSimpleSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods
    class Meta:
        model = Cook
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            # 'phone',
            # 'service_place',  
            # 'payment_address',
            # 'is_available',
            
        )
        # read_only_fields = ['rating', ]

class CourierForAddCourierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        
        model = Courier
        fields = (
            'id',
        )


class CourierForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'id',
            'username',
            'firstname',
            'lastname',
            'phone',
            'transport',
            # 'deliveryArea',
            # 'is_available',
            'location',
        )
        # extra_kwargs = {'transport': {'required': True}, 'work_experience': {'required': True}, 
        #                                                         'location': {'required': True}}
            
        # read_only_fields = ['rating'] 

class CourierSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'id',
            'username',
            'firstname',
            'lastname',
            # 'phone',
            'transport',
            # 'deliveryArea',
            'is_available',
            # 'location',
        )

class AddCourierSerializer(DynamicFieldsModelSerializer):
    courier = CourierForAddCourierSerializer(read_only=True)
    delivery_information = DeliveryAreaOrderForAddCourierSerializer(read_only=True)
    class Meta:
        model = Order
        fields = (
            'courier',
            'delivery_information',
        )


class RejectOrderSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Order
        fields = (
            'is_rejected',
            'reject_reason',   
        )

class ClientForOrderSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods
    class Meta:
        model = Client
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'patronymic',
            'phone_number',
            'email',
            'location',
        )

class ClientSimpleSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods
    class Meta:
        model = Client
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'patronymic',
            'location',
            # 'phone_number',
            # 'email',
        )

class OrderSimpleSerializer(DynamicFieldsModelSerializer):    #this one is changed
    cook = CookSimpleSerializer(required=False)
    courier = CourierSimpleSerializer(required=False)
    items = OrderItemForOrderSerializer(read_only=True, many=True)
    delivery_information = DeliveryAreaOrderSerializer(read_only=True, required=False)
    client = ClientSimpleSerializer(read_only=True, required=False)
    class Meta:
        model = Order
        fields = (
            'id',
            'is_active',
            'status',
            'order_total',
            'courier_status',
            'reject_reason',
            'reject_reason_courier',
            'cook',
            'courier',
            'delivery_information',
            'items',
            'client',
            'created_at',
            'updated_at',
        )

class OrderSimpleForClientSerializer(DynamicFieldsModelSerializer):    #this one is changed
    cook = CookSimpleSerializer(required=False)
    courier = CourierSimpleSerializer(required=False)
    items = OrderItemForOrderSerializer(read_only=True, many=True)
    # delivery_information = DeliveryAreaOrderSerializer(read_only=True, required=False)
    client = ClientSimpleSerializer(read_only=True, required=False)
    class Meta:
        model = Order
        fields = (
            'id',
            'is_active',
            'status',
            'order_total',
            # 'courier_status',
            'reject_reason',
            # 'reject_reason_courier',
            'cook',
            'courier',
            # 'delivery_information',
            'items',
            'client',
            'created_at',
            'updated_at',
        )


class OrderFullSerializer(DynamicFieldsModelSerializer):    #this one is changed
    cook = CookForOrderSerializer(required=False)
    courier = CourierForOrderSerializer(required=False)
    items = OrderItemForOrderSerializer(read_only=True, many=True)
    delivery_information = DeliveryAreaOrderSerializer(read_only=True, required=False)
    client = ClientForOrderSerializer(read_only=True, required=False)
    class Meta:
        model = Order
        fields = (
            'id',
            'is_active',
            'status',
            'courier_status',
            'reject_reason',
            'order_total',
            'cook',
            'courier',
            'delivery_information',
            'items',
            'client',
            'created_at',
            'updated_at',   
        )
        
class OrderFullForClientSerializer(DynamicFieldsModelSerializer):    #this one is changed
    cook = CookForOrderSerializer(required=False)
    courier = CourierForOrderSerializer(required=False)
    items = OrderItemForOrderSerializer(read_only=True, many=True)
    # delivery_information = DeliveryAreaOrderSerializer(read_only=True, required=False)
    client = ClientForOrderSerializer(read_only=True, required=False)
    class Meta:
        model = Order
        fields = (
            'id',
            'is_active',
            'status',
            # 'courier_status',
            'reject_reason',
            'order_total',
            'cook',
            'courier',
            # 'delivery_information',
            'items',
            'client',
            'created_at',
            'updated_at',   
        )