from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.http.response import Http404, JsonResponse
from cooks.models import Client, Cook
from delivery.api.serializers import CourierSerializer
from delivery.models import Courier, DeliveryPrice
from orders.api.serializers import AddCourierSerializer, OrderCreatSerializer, OrderFullSerializer, OrderItemCreateSerializer, OrderItemSerializer, OrderListSerializer, OrderSerializer, OrderUpdateSerializer, RejectOrderSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Order, OrderItem
from meals.models import Meal
from rest_framework import filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utility.check_token import checkToken

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', MealCreatSerializer)

# 'method' can be used to customize a single HTTP method of a view
# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(method = 'POST',request_body=OrderFullSerializer)
@api_view(['POST'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
def order_create(request):
    order_data = JSONParser().parse(request)

    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)

    try: 
        client1 = Client.objects.get(username = claimsOrMessage['Username']) 
    except Cook.DoesNotExist: 
        return JsonResponse({'Warning': 'You have not permission to create order with this token!'}, status=status.HTTP_200_OK)
    # create empty order with out orderItems, with customer data and add cook
    order_item_data = order_data['order_items']
    if not order_item_data:
        return JsonResponse({'message': "You can not create order without meal!"}, status=status.HTTP_200_OK)
    else:
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
            is_same_cook = True
            oneCookId = cook1.id
            print("****** oneCookId", oneCookId)
            for i in order_item_data:
                meal1_id = i['meal']
                meal1 = Meal.objects.get(pk=meal1_id)
                print("*****or item cook_id:", meal1.cook.id)
                print("*****or item title:", meal1.title)
                if meal1.cook.id != oneCookId:
                    is_same_cook = False
            print("****** is_same_cook", is_same_cook)
            if is_same_cook:
                order_serializer.save(cook = cook1, client = client1)
            else:
                return JsonResponse({'message': 'You have to choose meals from same cook!'}, status=status.HTTP_200_OK)            
        
        # get current order id for assigning to orderItem
        current_order_id = order_serializer.data['id']
        curren_order = Order.objects.get(pk=current_order_id)
        
        # get from data only order_item part
        order_item_data = order_data['order_items']
        
        # loop inside order items data and create several orderitems
            

        for i in order_item_data:
            print("i in order_item", i)
            # meal_id = i['meal']
            # meal = Meal.objects.get(pk=meal_id)
            # meal_quantity = i['quantity']
            # difference = meal.stock_quantity - meal_quantity
            # print("////// stock difference: ", difference)
            # if difference > 0:
            #     meal.stock_quantity = difference
            #     meal.save()
            # else:
            #     print("girdi else stok dif sohbeti")
            #     meal.stock_quantity = 0
            #     meal.save()
            # print("+++ meal quantity:", meal_quantity)
            orderItem_serializer = OrderItemCreateSerializer(data=i)
            if orderItem_serializer.is_valid():
                orderItem_serializer.save(order = curren_order)
        # f"Hello, {name}"
        return JsonResponse({'message': f"New order with {current_order_id} id is created succesfully"}, status=status.HTTP_201_CREATED)
        # return JsonResponse(order_serializer.data, status=status.HTTP_201_CREATED)

class OrderAPIView(generics.ListAPIView):
    
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = Order.objects.all()
    serializer_class = OrderFullSerializer

class OrderItemAPIView(generics.ListAPIView):
    
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


test_param_order = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)


@swagger_auto_schema(methods=['get'], manual_parameters=[test_param_order], responses={200: user_response_order}) 
# @swagger_auto_schema(methods=['delete'], manual_parameters=[test_param_order], responses={200: "order was deleted successfully"})
@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        order_serializer = OrderFullSerializer(order) 
        return JsonResponse(order_serializer.data)
    # elif request.method == 'DELETE':
    #     if order.complete == True: 
    #         order.delete() 
    #         return JsonResponse({'message': 'Order was deleted successfully!'}, status=status.HTTP_200_OK)
    #     else:
    #         return JsonResponse({'message': 'You can not delete this order, order not complete!'}, status=status.HTTP_403_FORBIDDEN)
    # elif request.method == 'PATCH':
    #     order_serializer = OrderFullSerializer(order, data=request.data, partial=True)
    #     if order_serializer.is_valid():
    #         order_serializer.save()
    #         return JsonResponse(order_serializer.data, status=status.HTTP_200_OK)
    #     return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=AddCourierSerializer, responses={200: "You assigned courier to order!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated]) #!
def add_courier_to_order(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    orderId = order.cook.id
    requestUserId = request.user.id
    request_data = JSONParser().parse(request)
    if isinstance(request.user, Cook) == False: #!
        return JsonResponse({'message': 'Only cook can add courier to order!'}, status=status.HTTP_200_OK)
    elif isinstance(request.user, Cook) != False and orderId != requestUserId:
        return JsonResponse({'message': 'You have not permission add courier to this order!'}, status=status.HTTP_200_OK)
    else:
        if order.is_rejected:
            return JsonResponse({'message': 'This order already rejected, You can not add couries to this order!'}, status=status.HTTP_200_OK)
        elif order.complete == True:
            return JsonResponse({'message': 'This order already completed, You can not add couries to this order!'}, status=status.HTTP_200_OK)
        elif order.courier != None:
            return JsonResponse({'message': 'This order already has courier!'}, status=status.HTTP_200_OK)


    
        # print("******//// order.items:", order.items.all())  
        courierId = request_data['courier']
        delivery_id = request_data['delivery_information']
        
        likedCourier = Courier.objects.filter(pk=courierId).first()
        choosen_delivery = DeliveryPrice.objects.filter(id=delivery_id).first()
        
        if choosen_delivery not in likedCourier.delivery_areas.all():
            return JsonResponse({"message": "This courier does not work in choosen delivery area!"}, status=status.HTTP_200_OK)
        # print("likedCourier.transport__isnull == True: ", likedCourier.transport)
        if likedCourier is None:
            return JsonResponse({"message": "Choosen courier does not exist!"}, status=status.HTTP_200_OK)

        elif likedCourier.is_available != True:
            return JsonResponse({'message': 'This courier is not available now!'}, status=status.HTTP_200_OK)

        elif likedCourier.transport == None or likedCourier.work_experience == None or likedCourier.delivery_areas == None:
            return JsonResponse({'message': 'This courier has not got enough information, please choose other courier!'}, status=status.HTTP_200_OK)    

        
        else:
            for i in order.items.all():
                # meal_id = i['meal']
                # meal = Meal.objects.get(pk=meal_id)
                # meal_quantity = i['quantity']
                difference = i.meal.stock_quantity - i.quantity
                print("////// stock difference: ", difference)
                if difference > 0:
                    i.meal.stock_quantity = difference
                    i.meal.save()
                else:
                    print("girdi else stok dif sohbeti")
                    i.meal.stock_quantity = 0
                    i.meal.save()
            print("Evvelce Curyerin statusu", likedCourier.is_available) 
            order.courier = likedCourier
            order.delivery_information = choosen_delivery

            # meal-in stokunu burda azaldiriq

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
            return JsonResponse({'message': 'You assigned courier to order!'}, status=status.HTTP_202_ACCEPTED)
        
        
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def complete_order(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    request_data = JSONParser().parse(request)
    order_items = order.items.all()
    cookId = None
    for i in order_items:
        cookId = i.meal.cook.id
    
    userInRequestId = request.user.id
    if isinstance(request.user, Cook) == False:
        return JsonResponse({'message': 'Only cook can complete order!'}, status=status.HTTP_200_OK)
    elif isinstance(request.user, Cook) == True and cookId != userInRequestId:
        return JsonResponse({'message': 'You have not permission complete this order!'}, status=status.HTTP_200_OK)
    elif isinstance(request.user, Cook) == True and cookId == userInRequestId:
        if order.is_rejected:
            return JsonResponse({'message': 'This order already rejected!'}, status=status.HTTP_200_OK)
        elif not order.courier:
            return JsonResponse({'message': 'This order has not courier yet, you can not complete this order!'}, status=status.HTTP_200_OK)
        elif order.complete:
            return JsonResponse({'message': 'You can not complete this order. This order already completed!'}, status=status.HTTP_200_OK)
        else:
            print("couriers id", order.courier.id)
            print("order.courier", order.courier)
            courierId = order.courier.id
            print(courierId)
            likedCourier = Courier.objects.get(pk=courierId)
            print("**************************")
            print("Evvelce complete-de Curyerin statusu", likedCourier.is_available)
            print("Evvelce complete-de Orderin statusu", order.complete)
            print("**************************")
            likedCourier.is_available = True
            order.complete = True
            likedCourier.save()
            order.save()
            print("Sonra complete-de Curyerin statusu", likedCourier.is_available)
            print("Sonra complete-de Orderin statusu", order.complete)
            print("**************************")
            return JsonResponse({'message': 'Order is completed!'}, status=status.HTTP_202_ACCEPTED)
            # order_serializer = OrderUpdateSerializer(order, data=request_data, partial=True)


test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=RejectOrderSerializer, responses={200: "Order is rejected!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def reject_order(request, pk):
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    request_data = JSONParser().parse(request)
    order_items = order.items.all()
    cookId = None
    userInRequestId = request.user.id
    for i in order_items:
        cookId = i.meal.cook.id
    if isinstance(request.user, Cook) == False:
        return JsonResponse({'message': 'Only cook can reject order!'}, status=status.HTTP_200_OK)
    elif isinstance(request.user, Cook) == True and cookId != userInRequestId:
        return JsonResponse({'message': 'You have not permission reject this order!'}, status=status.HTTP_200_OK)
    elif isinstance(request.user, Cook) == True and cookId == userInRequestId and order.complete:
        return JsonResponse({'message': 'You can not reject completed order!'}, status=status.HTTP_200_OK)
    elif order.courier:
        return JsonResponse({'message': 'You can not reject order after assigning courier!'}, status=status.HTTP_200_OK)
    else:
        print("**************")
        print("rejectde request_data", request_data)
        print("is rejected", request_data['is_rejected'])
        print("is rejected=True", request_data['is_rejected']==True)
        print("**************")
        if order.is_rejected:
            return JsonResponse({'message': 'This order already rejected!'}, status=status.HTTP_200_OK)
        elif order.complete:
            return JsonResponse({'message': 'You can not reject completed order!'}, status=status.HTTP_200_OK)
        elif request_data['is_rejected'] == True and not request_data['reject_reason']:
            return JsonResponse({'message': 'You can not reject with out reject reason information!'}, status=status.HTTP_200_OK)    
        else:
            order.is_rejected = True
            order.reject_reason = request_data['is_rejected']
            order.save()
            return JsonResponse({'message': f"Order with {order.id} id is rejected!"}, status=status.HTTP_200_OK)
    # if not order.courier:
    #     return JsonResponse({'message': 'This order has not courier yet, you can not complete this order!'}, status=status.HTTP_200_OK)
    # else:
    #     print("couriers id", order.courier.id)
    #     print("order.courier", order.courier)
    #     courierId = order.courier.id
    #     print(courierId)
    #     likedCourier = Courier.objects.get(pk=courierId)
    #     print("**************************")
    #     print("Evvelce complete-de Curyerin statusu", likedCourier.is_available)
    #     print("Evvelce complete-de Orderin statusu", order.complete)
    #     print("**************************")
    #     likedCourier.is_available = True
    #     order.complete = True
    #     likedCourier.save()
    #     order.save()
    #     print("Sonra complete-de Curyerin statusu", likedCourier.is_available)
    #     print("Sonra complete-de Orderin statusu", order.complete)
    #     print("**************************")
    #     return JsonResponse({'message': 'Order is completed!'}, status=status.HTTP_202_ACCEPTED)
    #     # order_serializer = OrderUpdateSerializer(order, data=request_data, partial=True)
    


    # if order_serializer.is_valid(raise_exception=True):
    #     order_serializer.save()
    # order_serializer.save()
    # return JsonResponse(order_serializer.data)

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

