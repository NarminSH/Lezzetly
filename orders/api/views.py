from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.http.response import Http404, JsonResponse
from orders.api.serializers import OrderCreatSerializer, OrderFullSerializer, OrderItemCreateSerializer, OrderListSerializer, OrderSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Order
from meals.models import Meal
from rest_framework import filters

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def order_create(request):
    order_data = JSONParser().parse(request)
    
    # create empty order with out orderItems, with customer data and add cook
    order_serializer = OrderFullSerializer(data=order_data)
    if order_serializer.is_valid():
            order_item_data = order_data['order_items']
            meal_id = None
            # get cook from meal
            for i in order_item_data:
               meal_id = i['meal']
            meal = Meal.objects.get(pk=meal_id)
            cook1 = meal.cook
            order_serializer.save(cook = cook1)
    
    # get current order id for assigning to orderItem
    current_order_id = order_serializer.data['id']
    curren_order = Order.objects.get(pk=current_order_id)
    
    # get from data only order_item part
    order_item_data = order_data['order_items']
    
    # loop inside order items data and create several orderitems
    for i in order_item_data:
        orderItem_serializer = OrderItemCreateSerializer(data=i)
        if orderItem_serializer.is_valid():
                orderItem_serializer.save(order = curren_order)
    
    return JsonResponse(order_serializer.data, status=status.HTTP_201_CREATED)

class OrderAPIView(generics.ListAPIView):
    
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = Order.objects.all()
    serializer_class = OrderFullSerializer

# class OrdersAPIView(ListCreateAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     queryset = Order.objects.all()
#     serializer_class = OrderListSerializer
#     lookup_url_kwarg = 'pk'

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return OrderSerializer
#         return super(OrdersAPIView, self).get_serializer_class()


# class OrderAPIView(RetrieveUpdateDestroyAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     queryset = Order.objects.all()

#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return OrderListSerializer     # for swagger file
#         return OrderSerializer

    # def get(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderListSerializer(
    #         order, context={'request': self.request})
    #     return JsonResponse(data=serializer.data, safe=False)

    # def put(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderSerializer(data=self.request.data,
    #                                    instance=order, context={'request': self.request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return JsonResponse(data=serializer.data, safe=False)

    # def delete(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderSerializer(order)
    #     order.delete()
    #     return JsonResponse(serializer.data, safe=False)

    # def patch(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     serializer = OrderSerializer(data=self.request.data, instance=order, 
    #                                 context={'request': self.request}, partial=True) # set partial=True to update a data partially
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return JsonResponse( data=serializer.data, safe=False)
    #     return JsonResponse( data="Wrong parameters")



# class OrderItemAPIView(RetrieveUpdateDestroyAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()
#     lookup_url_kwarg = 'pk'

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return OrderListSerializer
#         return super(OrderItemAPIView, self).get_serializer_class()


# class OrdersCompleteAPIView(GenericAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = OrderSerializer

#     def get(self, *args, **kwargs):
#         order = Order.objects.filter(complete=True).first()
#         if not order:
#             raise Http404
#         serializer = OrderSerializer(
#             order, context={'request': self.request})
#         return JsonResponse(data=serializer.data, safe=False)

