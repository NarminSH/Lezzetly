from django.http import request
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.http.response import Http404, JsonResponse
from cooks.models import Client, Cook
from delivery.api.serializers import CourierSerializer
from delivery.models import Courier, DeliveryPrice
from orders.api.serializers import AddCourierSerializer, OrderCreatSerializer, OrderFullForClientSerializer, OrderFullSerializer, OrderItemCreateSerializer, OrderItemSerializer, OrderListSerializer, OrderSerializer, OrderSimpleForClientSerializer, OrderSimpleSerializer, OrderUpdateSerializer, RejectOrderSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Order, OrderItem
from meals.models import Meal
from rest_framework import filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utility.check_token import checkToken
import logging

logger = logging.getLogger(__name__)

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
    print("Order create girdi")
    order_data = JSONParser().parse(request)
    

    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
    logger.info("just check logger")
    print("some print")
    # print("courier username", Client.objects.get(id=2).username)
    print("next some print")
    try: 
        client1 = Client.objects.get(username = claimsOrMessage['Username']) 
        # client1 = Courier.objects.get(id=4) 
    except: 
        return JsonResponse({'Warning': f'You have not permission to create order with this token!'}, status=status.HTTP_200_OK)
    # create empty order with out orderItems, with customer data and add cook
    
    order_item_data = order_data['order_items']
    logger.info("just check logger")
    print("order_item_data: ", order_item_data)
    
    if not order_item_data:
        return JsonResponse({'warning': "You can not create order without meal!"}, status=status.HTTP_200_OK)
    else:
        print("order_data", order_data)
        order_serializer = OrderFullSerializer(data=order_data)
        print("order_serializer: ", order_serializer)
        if order_serializer.is_valid():
            order_item_data = order_data['order_items']
            meal_id = None
            meal_quantity = None
            meal = None
            # get cook from meal
            for i in order_item_data:
                meal_id = i['meal']
                try:
                    meal = Meal.objects.get(pk=meal_id)
                except: 
                    return JsonResponse({'Warning': 'You try to order a not existing meal!'}, status=status.HTTP_200_OK)
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
                return JsonResponse({'warning': 'You have to choose meals from same cook!'}, status=status.HTTP_200_OK)            

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
        return JsonResponse({'message': f"New order with {current_order_id} id is created succesfully!"}, status=status.HTTP_201_CREATED)
        # return JsonResponse(order_serializer.data, status=status.HTTP_201_CREATED)

# class OrderAPIView(generics.ListAPIView):
    
#     authentication_classes = []
#     permission_classes = []
#     # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
#     # filter_backends = (filters.SearchFilter,)
#     queryset = Order.objects.all()
#     serializer_class = OrderFullSerializer

class OrderAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()

    def get(self, *args, **kwargs):
        logger.info("just check logger")

        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        print("In general active oreders api")
        if claimsOrMessage['Usertype'] == '1':
            print("kwargs.get('pk'): ", kwargs.get('pk'))
            # adminer de baxdim yaranan orderde complete false yox bos gorunur
            # orders = Order.objects.filter(cook=kwargs.get('pk'))
            # print("orders without false:", orders)
            orders = Order.objects.filter(cook=kwargs.get('pk'), is_active=False)
            print("orders with false:", orders)
            
            request_cook = Cook.objects.get(id = kwargs.get('pk')).username
            token_cook = claimsOrMessage['Username']
            print("request_cook:", request_cook)
            print("token_cook:", token_cook)
            if request_cook == token_cook:
                if not orders:
                    print("Bura girmedi")
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['cook'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)

        elif claimsOrMessage['Usertype'] == '2':
            orders = Order.objects.filter(courier=kwargs.get('pk'), is_active=False)
            request_courier = Courier.objects.get(id = kwargs.get('pk')).username
            token_courier = claimsOrMessage['Username']
            if request_courier == token_courier:
                if not orders:
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['courier'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)

        else:
            orders = Order.objects.filter(client=kwargs.get('pk'), is_active=False)
            request_client = Client.objects.get(id = kwargs.get('pk')).username
            token_client = claimsOrMessage['Username']
            if request_client == token_client:
                if not orders:
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['client'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)



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
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND) 
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

# @permission_classes([IsAuthenticated]) #!
@authentication_classes([])
@permission_classes([])
def add_courier_to_order(request, pk):

    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)

    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'warning': 'Only cook can add courier to order!'}, status=status.HTTP_200_OK)
    
    cookFromToken = claimsOrMessage['Username']

    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist:
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    cookInOrder = order.cook.username
    # requestUserId = request.user.id
    request_data = JSONParser().parse(request)
    # if isinstance(request.user, Cook) == False: #!
    #     return JsonResponse({'message': 'Only cook can add courier to order!'}, status=status.HTTP_200_OK)
    if cookFromToken != cookInOrder:
        return JsonResponse({'warning': 'You have not permission add courier to this order!'}, status=status.HTTP_200_OK)
    else:
        if order.status == "cook rejected order":
            return JsonResponse({'warning': 'This order already rejected by cook, You can not add couries to this order!'}, status=status.HTTP_200_OK)
        elif order.status == "order completed":
            return JsonResponse({'warning': 'This order already completed, You can not add couries to this order!'}, status=status.HTTP_200_OK)
        elif order.courier != None:
            return JsonResponse({'warning': 'This order already has courier!'}, status=status.HTTP_200_OK)

        # print("******//// order.items:", order.items.all())  
        courierId = request_data['courier']
        try:
            likedCourier = Courier.objects.get(pk=courierId)
        except Courier.DoesNotExist:
            return JsonResponse({'warning': f'Courier with this id {courierId} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # ******************** interesting not delete **********************
        delivery_id = request_data['delivery_information']
        
        choosen_delivery = DeliveryPrice.objects.filter(id=delivery_id).first()
        
        if choosen_delivery not in likedCourier.delivery_areas.all():
            return JsonResponse({"warning": "This courier does not work in choosen delivery area!"}, status=status.HTTP_200_OK)
        # print("likedCourier.transport__isnull == True: ", likedCourier.transport)
        # ******************** interesting not delete **********************
        # if likedCourier is None:
        #     return JsonResponse({"message": "Choosen courier does not exist!"}, status=status.HTTP_200_OK)
        
        if likedCourier.is_available != True:
            return JsonResponse({'warning': 'This courier is not available now!'}, status=status.HTTP_200_OK)

        elif likedCourier.transport == None or likedCourier.work_experience == None or likedCourier.delivery_areas == None:
            return JsonResponse({'warning': 'This courier has not got enough information, please choose other courier!'}, status=status.HTTP_200_OK)    
        # stock-dan cixma courierin accept hissesinde olmalidi
        else:
            # for i in order.items.all():
            #     difference = i.meal.stock_quantity - i.quantity
            #     print("////// stock difference: ", difference)
            #     if difference > 0:
            #         i.meal.stock_quantity = difference
            #         i.meal.save()
            #     else:
            #         print("girdi else stok dif sohbeti")
            #         i.meal.stock_quantity = 0
            #         i.meal.save()
            print("Evvelce Curyerin statusu", likedCourier.is_available) 
            order.courier = likedCourier
            order.courier_status = "cook sent request to courier"
            order.reject_reason = None
            order.delivery_information = choosen_delivery

            # meal-in stokunu burda azaldiriq

            # likedCourier.is_available = False
            
            # false etme courierin accept hissesinde olmalidi
            order.courier.is_available = False
            likedCourier.save()
            order.save()

            # print("Sonra Curyerin statusu", likedCourier.is_available)
            
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
# @permission_classes([IsAuthenticated])
@authentication_classes([])
@permission_classes([])
def complete_order(request, pk):
    print("entered to order complete!")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'warning': 'Only cook can complete order!'}, status=status.HTTP_200_OK)
    
    try: 
        order = Order.objects.get(pk=pk) 
    except Order.DoesNotExist: 
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_200_OK)
    
    request_data = JSONParser().parse(request)
    order_items = order.items.all()
    
    currentCookUsername = None
    for i in order_items:
        currentCookUsername = i.meal.cook.username
    
    cookInToken = claimsOrMessage['Username']
    # return JsonResponse({'warning': f'currentCookUsername: {currentCookUsername}! cookInToken: {cookInToken}'}, status=status.HTTP_200_OK)
    # if isinstance(request.user, Cook) == False:
    #     return JsonResponse({'message': 'Only cook can complete order!'}, status=status.HTTP_200_OK)
    if currentCookUsername != cookInToken:
        return JsonResponse({'warning': 'You have not permission complete this order!'}, status=status.HTTP_200_OK)
    elif currentCookUsername == cookInToken:
        if order.is_active == False:
            return JsonResponse({'warning': 'This order already not active!'}, status=status.HTTP_200_OK)
        elif not order.courier:
            return JsonResponse({'warning': 'This order has not courier yet, you can not complete this order!'}, status=status.HTTP_200_OK)
        elif order.status == "order completed":
            return JsonResponse({'warning': 'You can not complete this order. This order already completed!'}, status=status.HTTP_200_OK)
        else:
            # print("couriers id", order.courier.id)
            # print("order.courier", order.courier)
            courierId = order.courier.id
            # print(courierId)
            currentCourier = Courier.objects.get(pk=courierId)
            # print("**************************")
            # print("Evvelce complete-de Curyerin statusu", likedCourier.is_available)
            # print("Evvelce complete-de Orderin statusu", order.complete)
            # print("**************************")
            currentCourier.is_available = True
            order.is_active = False
            order.status = "order completed"
            currentCourier.save()
            order.save()
            # print("Sonra complete-de Curyerin statusu", likedCourier.is_available)
            # print("Sonra complete-de Orderin statusu", order.complete)
            # print("**************************")
            return JsonResponse({'warning': 'Order is completed, order is not active!'}, status=status.HTTP_202_ACCEPTED)
            # order_serializer = OrderUpdateSerializer(order, data=request_data, partial=True)


test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=RejectOrderSerializer, responses={200: "Order is rejected!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
def reject_order(request, pk):
    logger.info("just check logger")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] == "3":
        return JsonResponse({'warning': 'Client can not reject order!'}, status=status.HTTP_200_OK)

    try: 
        order = Order.objects.get(pk=pk)
        print("order", order)
    except Order.DoesNotExist: 
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_200_OK)
    request_data = JSONParser().parse(request)
    print(claimsOrMessage['Usertype'])
    if claimsOrMessage['Usertype'] == "1":
        print("order reject by cook firts step")
        order_items = order.items.all()
        currentCookUsername = None
        cookInToken = claimsOrMessage['Username']
        print("order reject by cook second step")
        for i in order_items:
            currentCookUsername = i.meal.cook.username
        # if isinstance(request.user, Cook) == False:
        #     return JsonResponse({'message': 'Only cook can reject order!'}, status=status.HTTP_200_OK)
        print("order reject by cook 2.5 step")
        if currentCookUsername != cookInToken:
            print("order reject by cook 2.6 step")
            return JsonResponse({'warning': 'You have not permission reject this order!'}, status=status.HTTP_200_OK)
        # elif currentCookUsername == cookInToken and order.status == "":
        #     return JsonResponse({'message': 'You can not reject completed order!'}, status=status.HTTP_200_OK)
        elif currentCookUsername == cookInToken and order.is_active:
            return JsonResponse({'warning': 'You can not reject order after accept!'}, status=status.HTTP_200_OK)
        # elif order.courier and not order.is_active:
        else:
            print("order reject by cook third step")
            # print("**************")
            # print("rejectde request_data", request_data)
            # print("is rejected", request_data['is_rejected'])
            # print("is rejected=True", request_data['is_rejected']==True)
            # print("**************")
            if order.status == "cook rejected order":
                return JsonResponse({'warning': 'This order already rejected!'}, status=status.HTTP_200_OK)
            elif order.is_active:
                return JsonResponse({'warning': 'You can not reject active order!'}, status=status.HTTP_200_OK)
            elif not request_data['reject_reason']:
                return JsonResponse({'warning': 'You can not reject without reject reason information!'}, status=status.HTTP_200_OK) 
            else:
                if order.courier:
                    print("rejectde courier-in olmasini yoxlayiriq")
                    print("courier.is_available: ", order.courier.is_available)
                    order.courier.is_available = True
                    order.courier.save()
                    print("courier.is_available true edenden sonra: ", order.courier.is_available)
                    order.courier_status = "cook rejected order"
                order.status = "cook rejected order"
                order.reject_reason = request_data['reject_reason']
                order.save()
                return JsonResponse({'message': f"Order with {order.id} id is rejected, resaon: {order.reject_reason}"}, status=status.HTTP_200_OK)
    elif claimsOrMessage['Usertype'] == "2":
        courierUsernameInToken = claimsOrMessage['Username']
        try:
            currentCourier = Courier.objects.get(username=courierUsernameInToken)
            print("currentCourier", currentCourier)
        except Courier.DoesNotExist: 
            return JsonResponse({'warning': 'You have not permissio reject order with this token!'}, status=status.HTTP_200_OK)
        print("order.courier.username", order.courier.username)
        if order.courier.username != courierUsernameInToken:
            return JsonResponse({'warning': 'You have not permissio reject order with this token!'}, status=status.HTTP_200_OK)
        print("request_data['reject_reason']", request_data['reject_reason'])
        if not request_data['reject_reason']:
            return JsonResponse({'warning': 'You can not reject without reject reason information!'}, status=status.HTTP_200_OK)
        print("order.courier", order.courier)
        order.courier.is_available = True
        order.courier.save()
        order.courier = None
        print("order.reject_reason", order.reject_reason)
        order.reject_reason = request_data['reject_reason']
        print("order.courier_status", order.courier_status)
        order.courier_status = "courier reject order"
        order.save()
        print("sonra order.courier", order.courier)
        return JsonResponse({'message': f"Order with {order.id} id is rejected by Courier({currentCourier}), resaon: {order.reject_reason}"}, status=status.HTTP_200_OK)

test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=RejectOrderSerializer, responses={200: "Order is rejected!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
def accept_order(request, pk):
    logger.info("just check logger")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] == "3":
        return JsonResponse({'warning': 'Client can not accept order!'}, status=status.HTTP_200_OK)

    try: 
        order = Order.objects.get(pk=pk)
        print("order", order)
    except Order.DoesNotExist: 
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_200_OK)
    request_data = JSONParser().parse(request)
    print(claimsOrMessage['Usertype'])
    if claimsOrMessage['Usertype'] == "1":
        # print("order reject by cook firts step")
        order_items = order.items.all()
        currentCookUsername = None
        cookInToken = claimsOrMessage['Username']
        # print("order reject by cook second step")
        for i in order_items:
            currentCookUsername = i.meal.cook.username
        # if isinstance(request.user, Cook) == False:
        #     return JsonResponse({'message': 'Only cook can reject order!'}, status=status.HTTP_200_OK)
        # print("order reject by cook 2.5 step")
        if currentCookUsername != cookInToken:
            # print("order reject by cook 2.6 step")
            return JsonResponse({'warning': 'You have not permission accept this order!'}, status=status.HTTP_200_OK)
        # elif currentCookUsername == cookInToken and order.status == "":
        #     return JsonResponse({'message': 'You can not reject completed order!'}, status=status.HTTP_200_OK)
        elif currentCookUsername == cookInToken and order.is_active:
            return JsonResponse({'warning': 'You already accept this order!'}, status=status.HTTP_200_OK)
        # elif order.courier and not order.is_active:
        else:
            # print("order reject by cook third step")
            # print("**************")
            # print("rejectde request_data", request_data)
            # print("is rejected", request_data['is_rejected'])
            # print("is rejected=True", request_data['is_rejected']==True)
            # print("**************")
            if order.reject_reason is not None:
                return JsonResponse({'warning': 'You can not accept rejected order!'}, status=status.HTTP_200_OK)
            elif order.courier_status != "courier accept order" and order.courier_status != "courier accept order and wait confirmation of cook":
                return JsonResponse({'warning': 'This order have not courier or courier not accept order yet!'}, status=status.HTTP_200_OK)
            else:
                zero_meal = False
                for i in order.items.all():
                    if i.meal.stock_quantity == 0:
                        zero_meal = True
                    difference = i.meal.stock_quantity - i.quantity
                    
                    print("////// stock difference: ", difference)
                    if difference > 0 or difference == 0:
                        i.meal.stock_quantity = difference
                        i.meal.save()
                    else:
                        print("girdi else stok dif sohbeti")
                        i.meal.stock_quantity = 0
                        zero_meal = True
                        i.meal.save()
                order.courier_status = "cook accept courier"
                if zero_meal:
                    order.status = "cook is preparing your order"
                else:
                    order.status = "courier is on the way to order"

                order.is_active = True
                order.save()
                return JsonResponse({'message': f"Order with {order.id} id is accepted by cook, order is active now!"}, status=status.HTTP_200_OK)
    elif claimsOrMessage['Usertype'] == "2":
        print("courier-e aid hisseye girdu")
        courierUsernameInToken = claimsOrMessage['Username']
        try:
            currentCourier = Courier.objects.get(username=courierUsernameInToken)
            # print("currentCourier", currentCourier)
        except Courier.DoesNotExist: 
            return JsonResponse({'warning': 'You have not permission accept order with this token!'}, status=status.HTTP_200_OK)
        # print("order.courier.username", order.courier.username)
        if not order.courier.username:
            return JsonResponse({'warning': 'This order have not courier!'}, status=status.HTTP_200_OK)
        if order.courier.username != courierUsernameInToken:
            return JsonResponse({'warning': 'You have not permission accept order with this token!'}, status=status.HTTP_200_OK)
        order.courier_status = "courier accept order and wait confirmation of cook"
        order.save()
        return JsonResponse({'message': f"Order with {order.id} id is accepted by courier ({currentCourier})"}, status=status.HTTP_200_OK)


test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=RejectOrderSerializer, responses={200: "Order is rejected!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
def pick_order(request, pk):
    logger.info("just check logger")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "2":
        return JsonResponse({'warning': 'Only Courier can pick order!'}, status=status.HTTP_200_OK)

    try: 
        order = Order.objects.get(pk=pk)
        print("order", order)
    except Order.DoesNotExist: 
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_200_OK)
    request_data = JSONParser().parse(request)
    # print(claimsOrMessage['Usertype'])
    
    if claimsOrMessage['Usertype'] == "2":
        print("courier-e aid hisseye girdu")
        courierUsernameInToken = claimsOrMessage['Username']
        try:
            currentCourier = Courier.objects.get(username=courierUsernameInToken)
            # print("currentCourier", currentCourier)
        except Courier.DoesNotExist: 
            return JsonResponse({'warning': 'You have not permission pick order with this token!'}, status=status.HTTP_200_OK)
        # print("order.courier.username", order.courier.username)
        if order.courier.username != courierUsernameInToken:
            return JsonResponse({'warning': 'You have not permission pick up order with this token!'}, status=status.HTTP_200_OK)
        if order.is_active == False:
            return JsonResponse({'warning': 'You can not pick up not active order!'}, status=status.HTTP_200_OK)
        order.status = "courier on the way to client"
        order.save()
        return JsonResponse({'message': f"Order with {order.id} id is picked by {currentCourier}"}, status=status.HTTP_200_OK)


test_param_order_adc = openapi.Parameter('order', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
# user_response_order = openapi.Response('Asagidaki Melumatlar qayidir', OrderFullSerializer)
@swagger_auto_schema(method='patch', manual_parameters=[test_param_order_adc],request_body=RejectOrderSerializer, responses={200: "Order is rejected!"})
# @swagger_auto_schema(method = 'patch',request_body=AddCourierSerializer)
@api_view(['PATCH'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
def deliver_order(request, pk):
    logger.info("just check logger")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "2":
        return JsonResponse({'warning': 'Only Courier can deliver order!'}, status=status.HTTP_200_OK)

    try: 
        order = Order.objects.get(pk=pk)
        print("order", order)
    except Order.DoesNotExist: 
        return JsonResponse({'warning': 'The order does not exist'}, status=status.HTTP_200_OK)
    request_data = JSONParser().parse(request)
    # print(claimsOrMessage['Usertype'])
    
    if claimsOrMessage['Usertype'] == "2":
        print("courier-e aid hisseye girdu")
        courierUsernameInToken = claimsOrMessage['Username']
        try:
            currentCourier = Courier.objects.get(username=courierUsernameInToken)
            # print("currentCourier", currentCourier)
        except Courier.DoesNotExist: 
            return JsonResponse({'warning': 'You have not permission deliver order with this token!'}, status=status.HTTP_200_OK)
        # print("order.courier.username", order.courier.username)
        if order.courier.username != courierUsernameInToken:
            return JsonResponse({'warning': 'You have not permission deliver order with this token!'}, status=status.HTTP_200_OK)
        if order.is_active == False:
            return JsonResponse({'warning': 'You can not deliver not active order!'}, status=status.HTTP_200_OK)
        order.status = "order delivered"
        order.save()
        return JsonResponse({'message': f"Order with {order.id} id is delivered to client by ({currentCourier})"}, status=status.HTTP_200_OK)



class ActiveOrdersAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):
        logger.info("just check logger")

        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        print("In general active orders api")
        if claimsOrMessage['Usertype'] == '1':
            try:
                request_cook = Cook.objects.get(id = kwargs.get('pk')).username
            except Cook.DoesNotExist:
                return JsonResponse({"Warning": "Cook does not exist"})
            token_cook = claimsOrMessage['Username']
            print("request_cook:", request_cook)
            print("token_cook:", token_cook)
            if request_cook == token_cook:
                orders = Order.objects.filter(cook=kwargs.get('pk'), is_active=True)
                if not orders:
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['cook'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)

        elif claimsOrMessage['Usertype'] == '2':
            try:
                request_courier = Courier.objects.get(id = kwargs.get('pk')).username
            except Courier.DoesNotExist:
                return JsonResponse({"Warning": "Courier does not exist"})
            token_courier = claimsOrMessage['Username']
            if request_courier == token_courier:
                orders = Order.objects.filter(courier=kwargs.get('pk'), is_active=True)
                if not orders:
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['courier'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)

        else:
            try:
                request_client = Client.objects.get(id = kwargs.get('pk')).username
            except Client.DoesNotExist:
                return JsonResponse({"Warning": "Client does not exist"})
            token_client = claimsOrMessage['Username']
            if request_client == token_client:
                orders = Order.objects.filter(client=kwargs.get('pk'), is_active=True)
                if not orders:
                    return JsonResponse ({'Warning': "You don't have ongoing order"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderFullForClientSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['client'])
                return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse ({"Warning": "You can not look at others' profile"}, status=status.HTTP_200_OK)




class UserOrders(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSimpleSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):

        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        
        if claimsOrMessage['Usertype'] == '1':
            try:
                request_cook = Cook.objects.get(id = kwargs.get('pk')).username
            except Cook.DoesNotExist:
                return JsonResponse({"Warning": "Cook does not exist"})
            orders = Order.objects.filter(cook=kwargs.get('pk'), is_active=False)
            token_cook = claimsOrMessage['Username']
            if request_cook == token_cook:
                if not orders:
                    return JsonResponse ({'Warning': "You don't have not active orders"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderSimpleSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['cook'])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse ({"Warning": "You can not look at others' profile"})

        elif claimsOrMessage['Usertype'] == '2':
            try:
                request_courier = Courier.objects.get(id = kwargs.get('pk')).username
            except Courier.DoesNotExist:
                return JsonResponse({"Warning": "Courier does not exist"})
            token_courier = claimsOrMessage['Username']
            if request_courier == token_courier:
                orders = Order.objects.filter(courier=kwargs.get('pk'), is_active=False)
                if not orders:
                    return JsonResponse ({'Warning': "You don't have not active orders"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderSimpleSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['courier'])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse ({"Warning": "You can not look at others' profile"})

        else:
            try:
                request_client = Client.objects.get(id = kwargs.get('pk')).username
            except Client.DoesNotExist:
                return JsonResponse({"Warning": "Client does not exist"})
            token_client = claimsOrMessage['Username']
            if request_client == token_client:
                orders = Order.objects.filter(client=kwargs.get('pk'), is_active=False)
                if not orders:
                    return JsonResponse ({'Warning': "You don't have not active orders"}, status=status.HTTP_200_OK, safe=False)
                serializer = OrderSimpleForClientSerializer(
                    orders, many=True, context={'request': self.request}, exclude=['client', 'courier'])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse ({"Warning": "You can not look at others' profile"})
