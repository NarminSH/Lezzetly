
from django.db.models.query import QuerySet
from django.http.response import Http404, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt
from rest_framework import filters
from django_filters import rest_framework as djangofilters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import  status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from delivery.api.serializers import CourierSerializer, DeliveryAreaPriceListSerializer, DeliveryAreaPriceSerializer, DeliveryAreaSerializer, ShortCourierCreateSerializer
from delivery.models import Courier, DeliveryArea, DeliveryPrice
from orders.api.serializers import OrderFullSerializer, OrderSimpleSerializer
from orders.models import Order
from django.conf import settings

from utility.check_token import checkToken

class CouriersAPIView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Courier.objects.filter(is_available=True)
    serializer_class = CourierSerializer


# class CourierOrdersAPIView(ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = OrderFullSerializer
#     queryset = Order.objects.all()

#     def get(self, *args, **kwargs):
#             item = Order.objects.filter(courier=kwargs.get('pk'), complete=True)
#             if self.request.user.id == kwargs.get('pk'): 
#                 if not item:
#                     return JsonResponse (data=[], status=200, safe=False)
#                 serializer = OrderFullSerializer(
#                     item, many=True, context={'request': self.request}, exclude=["courier"])
#                 return JsonResponse(data=serializer.data, safe=False)
#             return JsonResponse (data="You do not have permissions to look at others !", status=403, safe=False)


class CourierOrdersAPIView(ListAPIView):   #changed all api views to generic ones bcz of swagger documentation
    # authentication_classes = []
    # permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSimpleSerializer
    queryset = Order.objects.all()

    def get(self, *args, **kwargs):
        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        if claimsOrMessage['Usertype'] != '2':
            return JsonResponse({'Warning': 'You have not permission to get couriers orders!'}, status=status.HTTP_200_OK)    

        orders = Order.objects.filter(courier=kwargs.get('pk'))
        cookFromReqParam = Courier.objects.get(id = kwargs.get('pk')).username
        cookFromToken = claimsOrMessage['Username']
        if cookFromReqParam == cookFromToken:
            if not orders:
                return JsonResponse ({'Warning': 'This courier have not any orders!'}, status=status.HTTP_200_OK, safe=False)
            serializer = OrderSimpleSerializer(
                orders, many=True, context={'request': self.request}, exclude=['courier'])
            return JsonResponse(data=serializer.data, safe=False)
        return JsonResponse({'Warning': 'You have not permission to get other couriers orders!'}, safe=False, status=status.HTTP_200_OK)


# class CourierActiveOrdersAPIView(ListAPIView):
#     # authentication_classes = []
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = OrderFullSerializer
#     queryset = Order.objects.all()

#     def get(self, *args, **kwargs):
#             item = Order.objects.filter(courier=kwargs.get('pk'), complete=False)
#             print(self.request.user)
#             if self.request.user.id == kwargs.get('pk'): 
#                 if not item:
#                     return JsonResponse (data=[], status=200, safe=False)
#                 serializer = OrderFullSerializer(
#                     item, many=True, context={'request': self.request}, exclude=["courier"])
#                 return JsonResponse(data=serializer.data, safe=False)
#             return JsonResponse (data="You do not have permissions to look at others orders!", status=403, safe=False)

class CourierActiveOrdersAPIView(ListAPIView):   #changed all api views to generic ones bcz of swagger documentation
    # authentication_classes = []
    # permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()

    def get(self, *args, **kwargs):
        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        if claimsOrMessage['Usertype'] != '2':
            return JsonResponse({'Warning': 'You have not permission to get couriers orders!'}, status=status.HTTP_200_OK)    

        orders = Order.objects.filter(courier=kwargs.get('pk'), complete=False, is_rejected=False)
        cookFromReqParam = Courier.objects.get(id = kwargs.get('pk')).username
        cookFromToken = claimsOrMessage['Username']
        if cookFromReqParam == cookFromToken:
            if not orders:
                return JsonResponse ({'Warning': 'This courier have not any orders!'}, status=status.HTTP_200_OK, safe=False)
            serializer = OrderFullSerializer(
                orders, many=True, context={'request': self.request}, exclude=['courier'])
            return JsonResponse(data=serializer.data, safe=False)
        return JsonResponse({'Warning': 'You have not permission to get other couriers orders!'}, safe=False, status=status.HTTP_200_OK)


class CourierAreasAPIView(ListCreateAPIView):
    # authentication_classes = []
    # permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = DeliveryAreaPriceSerializer
    queryset = DeliveryPrice.objects.all()

    def get(self, *args, **kwargs):
        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        if claimsOrMessage['Usertype'] != '2' and claimsOrMessage['Usertype'] != '1':
            return JsonResponse({'Warning': 'You have not permission to get courier delivery areas!'}, status=status.HTTP_200_OK)

        item = DeliveryPrice.objects.filter(courier=kwargs.get('pk'))
        if not item:
            return JsonResponse ({'Warning': 'You have not any delivery area!'}, status=status.HTTP_200_OK, safe=False)
        serializer = DeliveryAreaPriceListSerializer(
            item, many=True, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        delivery_data = self.request.data

        tokenStr = self.request.META.get('HTTP_AUTHORIZATION')
        claimsOrMessage = checkToken(tokenStr)
        if 'warning' in claimsOrMessage:
            return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
        
        if claimsOrMessage['Usertype'] != '2':
            return JsonResponse({'Warning': 'You have not permission to create delivery areas!'}, status=status.HTTP_200_OK)
        currentCourier = Courier.objects.get(id = kwargs.get('pk'))
        courierFromToken = claimsOrMessage['Username']
        if currentCourier.username == courierFromToken:
            serializer = DeliveryAreaPriceSerializer(data=delivery_data, context={
                                            'request': self.request})
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data['courier']= currentCourier
            serializer.save(courier = currentCourier)
            return JsonResponse(data=serializer.data, safe=False, status=201)
        return JsonResponse ({'Warning': 'You have not permission to create delivery area for other courier!'}, status=status.HTTP_200_OK, safe=False)


test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@swagger_auto_schema(method = 'POST',request_body=ShortCourierCreateSerializer)
@parser_classes([JSONParser, MultiPartParser])
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def courierCreate(request):
    cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
    
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)

    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
   
    if claimsOrMessage['Usertype'] != '2':
        return JsonResponse({'Warning': 'You have not permission to create courier!'}, status=status.HTTP_200_OK)    
    courier_serializer = ShortCourierCreateSerializer(data=cook_data)
    try:
        currentCook = Courier.objects.get(username = claimsOrMessage['Username'])
        return JsonResponse({'Warning': f'The courier with this username({currentCook.username}) already exists!'}, status=status.HTTP_200_OK)
    except Courier.DoesNotExist:
        if courier_serializer.is_valid():
            courier_serializer.save(username = claimsOrMessage['Username'], user_type = claimsOrMessage['Usertype'])
            return JsonResponse({'Message': f"Courier with id {courier_serializer.data['id']} is successfully created!"}, status=status.HTTP_200_OK) 
        elif 'email' in courier_serializer.errors and 'username'in courier_serializer.errors:
            print(courier_serializer.errors)
            return JsonResponse({'warning': 'cook with this username and email already exists!'}, status=status.HTTP_200_OK)
        elif 'email' in courier_serializer.errors:
            return JsonResponse({'warning': 'cook with this email already exists!'}, status=status.HTTP_200_OK)
        elif 'username' in courier_serializer.errors:
            return JsonResponse({'warning': 'cook with this username already exists!'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(courier_serializer.errors, status=status.HTTP_200_OK)



test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual parametrs", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('Get information about single cook with id', CourierSerializer)
put_response = openapi.Response('Change information about single cook with id', CourierSerializer)

# 'method' can be used to customize a single HTTP method of a view
@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['put', 'PATCH', 'DELETE'], request_body=CourierSerializer, responses={200: put_response})
@parser_classes([JSONParser, MultiPartParser])
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
# @authentication_classes([])  # if enable this decorator user will always be anonymous and without this decorator user has to login even for get method
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
def courier_detail(request, pk):
    print("Daxil oldu courier_detail-a")
    try: 
        courier = Courier.objects.get(pk=pk) 
    except Courier.DoesNotExist: 
        return JsonResponse({'Warning': 'The courier does not exists.'}, status=status.HTTP_200_OK) 

    courier_data = JSONParser().parse(request) # don't forget you are able to send only json data
    
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)

    if request.method == 'GET':
        if claimsOrMessage['Username'] == courier.username and claimsOrMessage['Usertype'] == "2":  
            courier_serializer = CourierSerializer(courier)
            return JsonResponse(courier_serializer.data)
        # courier_serializer = CourierSerializer(courier) 
        else:
            return JsonResponse({'Warning': 'You have not permission to get this courier info!'}, status=status.HTTP_200_OK) 

    elif request.method == 'PUT': 
        if claimsOrMessage['Username'] == courier.username and claimsOrMessage['Usertype'] == "2":
            # cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            print("courier_data: ", courier_data)
            if 'username' in courier_data:
                if courier_data['username'] != claimsOrMessage['Username']:
                    return JsonResponse({'Warning': 'You can not change username!'}, status=status.HTTP_200_OK)
            if 'user_type' in courier_data:
                if courier_data['user_type'] != claimsOrMessage['Usertype']:
                    return JsonResponse({'Warning': 'You can not change user_type!'}, status=status.HTTP_200_OK)
            courier_serializer = CourierSerializer(courier, data=courier_data)
            if courier_serializer.is_valid(): 
                courier_serializer.save() 
                return JsonResponse(courier_serializer.data)
            
            elif 'email' in courier_serializer.errors:
                return JsonResponse({'warning': 'Courier with this email address already exists.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(courier_serializer.errors, status=status.HTTP_200_OK) 
        return JsonResponse({'warning': 'You have no rights to change this courier!'}, status=status.HTTP_200_OK)

    elif request.method == 'PATCH': 
        if claimsOrMessage['Username'] == courier.username and claimsOrMessage['Usertype'] == "2":
            # cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            if 'username' in courier_data:
                if courier_data['username'] != claimsOrMessage['Username']:
                    return JsonResponse({'Warning': 'You can not change username!'}, status=status.HTTP_200_OK)
            if 'user_type' in courier_data:
                if courier_data['user_type'] != claimsOrMessage['Usertype']:
                    return JsonResponse({'Warning': 'You can not change user_type!'}, status=status.HTTP_200_OK)
            courier_serializer = CourierSerializer(courier, data=courier_data, partial=True) 
            if courier_serializer.is_valid(): 
                courier_serializer.save() 
                return JsonResponse(courier_serializer.data)
            elif 'email' in courier_serializer.errors:
                return JsonResponse({'warning': 'Courier with this email address already exists.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(courier_serializer.errors, status=status.HTTP_200_OK) 
        return JsonResponse({'warning': 'You have no rights to change this courier!'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if claimsOrMessage['Username'] == courier.username and claimsOrMessage['Usertype'] == "2":
            all_orders = courier.orders.all()
            ongoing_orders = 0
            if all_orders:
                for order in all_orders:
                    if order.complete == False:
                        ongoing_orders += 1
                if ongoing_orders == 0:
                    courier.delete()   
                    return JsonResponse({'message': 'The cook was deleted successfully!'}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'warning': 'You have ongoing order!'}, status=status.HTTP_200_OK)
        return JsonResponse({'warning': 'You have no rights to delete the courier!'}, status=status.HTTP_200_OK)   #changed status fromm 200 to 403
    

# class CourierAPIView(RetrieveUpdateDestroyAPIView):
#     # authentication_classes = []
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     queryset = Courier.objects.all()
#     lookup_url_kwarg = 'pk'
#     serializer_class = CourierSerializer

#     def put(self, *args, **kwargs):
#         courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
#         if courier != self.request.user:
#             return JsonResponse({'message': 'Only courier himself can update the courier!'}, status=status.HTTP_403_FORBIDDEN)
#         if not courier:
#             return JsonResponse (data=[], status=200, safe=False)
#         serializer = CourierSerializer(data=self.request.data,
#                                        instance=courier, context={'request': self.request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return JsonResponse(data=serializer.data, safe=False)

#     def delete(self, *args, **kwargs):
#         courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
#         if courier != self.request.user:
#             return JsonResponse({'message': 'Only courier himself can delete the courier!'}, status=status.HTTP_403_FORBIDDEN)
#         if not courier:
#             return JsonResponse (data=[], status=200, safe=False)
#         serializer = CourierSerializer(courier)
#         courier.delete()
#         print('deleteddd')
#         print(serializer.data)
#         # return JsonResponse(data="Courier is deleted successfully!", safe=False)
#         return JsonResponse({'message': 'Courier is deleted successfully!'}, status=status.HTTP_200_OK)

#     def patch(self, *args, **kwargs):
#         courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
#         if courier != self.request.user:
#             return JsonResponse({'message': 'Only courier himself can update the courier!!'}, status=status.HTTP_200_OK)
#         serializer = CourierSerializer(data=self.request.data, instance=courier, 
#                                     context={'request': self.request}, partial=True) # set partial=True to update a data partially
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return JsonResponse( data=serializer.data, safe=False)
#         return JsonResponse( data="Wrong parameters")



class DeliveryAreasAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = DeliveryArea.objects.all()
    serializer_class = DeliveryAreaSerializer 


class CourierAreaAPIView(RetrieveUpdateDestroyAPIView): #this view is to change certain datas of particular courier
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = DeliveryPrice.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeliveryAreaPriceListSerializer     # for swagger file
        return DeliveryAreaPriceSerializer

    def put(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        delivery_area = DeliveryPrice.objects.filter(pk=kwargs.get('id')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'Only courier himself can update the courier area!!'}, status=status.HTTP_200_OK)
        if not courier:
            return JsonResponse (data=[], status=200, safe=False)
        serializer = DeliveryAreaPriceSerializer(data=self.request.data,
                                       instance=delivery_area, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['courier']= self.request.user
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False)
    
    def delete(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        delivery_area = DeliveryPrice.objects.filter(pk=kwargs.get('id')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'Only courier himself can delete the delivery area!'}, status=status.HTTP_403_FORBIDDEN)
        if not courier:
            return JsonResponse (data=[], status=200, safe=False)
        delivery_area.delete()
        return JsonResponse({'message': 'Delivery area is deleted successfully!'}, status=status.HTTP_200_OK)



class CouriersDeliveryAreasAPIView(ListAPIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = DeliveryPrice.objects.all()
    serializer_class = DeliveryAreaPriceListSerializer