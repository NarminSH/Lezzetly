from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.http.response import Http404, JsonResponse
from delivery.api.serializers import CourierSerializer
from delivery.models import Courier
from orders.api.serializers import OrderCreatSerializer, OrderFullSerializer, OrderItemCreateSerializer, OrderListSerializer, OrderSerializer, OrderUpdateSerializer
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
            meal_quantity = None
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
        meal_id = i['meal']
        meal = Meal.objects.get(pk=meal_id)
        meal_quantity = i['quantity']
        difference = meal.stock_quantity - meal_quantity
        if difference > 0:
            meal.stock_quantity = difference
        else:
            meal.stock_quantity = 0
        # print("+++ meal quantity:", meal_quantity)
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



@api_view(['GET', 'DELETE', 'PATCH'])
@authentication_classes([])
@permission_classes([AllowAny])
def order_detail(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        order_serializer = OrderFullSerializer(order) 
        return JsonResponse(order_serializer.data)
    elif request.method == 'DELETE':
        if order.complete == True: 
            order.delete() 
            return JsonResponse({'message': 'meal was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'message': 'You can not delete this order, order not complete!'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PATCH':
        order_serializer = OrderFullSerializer(order, data=request.data, partial=True)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse(order_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['PATCH'])
@authentication_classes([])
@permission_classes([AllowAny])
def add_courier_to_order(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    request_data = JSONParser().parse(request)
    
    courierId = request_data['courier']
    
    likedCourier = Courier.objects.get(pk=courierId)

    print("Evvelce Curyerin statusu", likedCourier.is_available)
    
    order.courier = likedCourier
    # likedCourier.is_available = False
    order.courier.is_available = False
    likedCourier.save()
    order.save()

    print("Sonra Curyerin statusu", likedCourier.is_available)
      
    # curier_serializer = CourierSerializer(likedCourier, )
    # order_serializer = OrderFullSerializer(order, data=request_data, partial=True)
    # order_serializer = OrderUpdateSerializer(order, data=request_data, partial=True)

    # if order_serializer.is_valid(raise_exception=True):
    #     order_serializer.save()
    # return JsonResponse(order_serializer.data)
    return JsonResponse({'message': 'You assign courier to order!'}, status=status.HTTP_202_ACCEPTED)
    
@api_view(['PATCH'])
@authentication_classes([])
@permission_classes([AllowAny])
def complete_order(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    request_data = JSONParser().parse(request)
    print(request_data['courier'])
    courierId = request_data['courier']
    print(courierId)
    likedCourier = Courier.objects.get(pk=courierId)
    likedCourier.is_available = True
    order.complete = True
    order_serializer = OrderUpdateSerializer(order, data=request_data, partial=True)

    if order_serializer.is_valid(raise_exception=True):
        order_serializer.save()
    order_serializer.save()
    return JsonResponse(order_serializer.data)

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

