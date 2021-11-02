
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
from orders.api.serializers import OrderFullSerializer
from orders.models import Order
from django.conf import settings

class CouriersAPIView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # queryset = Courier.objects.filter(is_available=True, transport__isnull=False, 
    #                         rating__isnull=False, work_experience__isnull=False, deliveryArea__isnull=False )
    
    # search_fields = ('delivery_areas__area__area_name',)
    # filter_backends = (djangofilters.DjangoFilterBackend, filters.SearchFilter)
    queryset = Courier.objects.filter(is_available=True)
    serializer_class = CourierSerializer


class CourierOrdersAPIView(ListAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):
            item = Order.objects.filter(courier=kwargs.get('pk'), complete=True)
            if self.request.user.id == kwargs.get('pk'): 
                if not item:
                    return JsonResponse (data=[], status=200, safe=False)
                serializer = OrderFullSerializer(
                    item, many=True, context={'request': self.request}, exclude=["courier"])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse (data="You do not have permissions to look at others !", status=403, safe=False)



class CourierActiveOrdersAPIView(ListAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):
            item = Order.objects.filter(courier=kwargs.get('pk'), complete=False)
            print(self.request.user)
            if self.request.user.id == kwargs.get('pk'): 
                if not item:
                    return JsonResponse (data=[], status=200, safe=False)
                serializer = OrderFullSerializer(
                    item, many=True, context={'request': self.request}, exclude=["courier"])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse (data="You do not have permissions to look at others orders!", status=403, safe=False)


class CourierAreasAPIView(ListCreateAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DeliveryAreaPriceSerializer
    queryset = DeliveryPrice.objects.all()

    def get(self, *args, **kwargs):
            item = DeliveryPrice.objects.filter(courier=kwargs.get('pk'))
            if not item:
                return JsonResponse (data=[], status=200, safe=False)
            serializer = DeliveryAreaPriceListSerializer(
                item, many=True, context={'request': self.request}, exclude =['courier'])
            return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        delivery_data = self.request.data
        if self.request.user.id == kwargs.get('pk'): 
            serializer = DeliveryAreaPriceSerializer(data=delivery_data, context={
                                            'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['courier']= self.request.user
            serializer.save()
            return JsonResponse(data=serializer.data, safe=False, status=201)
        return JsonResponse (data="You do not have permissions to create delivery area for this courier!", status=403, safe=False)


test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@swagger_auto_schema(method = 'POST',request_body=ShortCourierCreateSerializer)
@parser_classes([JSONParser, MultiPartParser])
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def courierCreate(request):
    # token = request.data['Token']

    # print("Token: ", token)
    print("Daxil oldu CourierCreate-e")
    # print("request******", request.user)
    # print("cook-create usertype:", usertype)
    # x = isinstance(5, int)
    cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    bearerToken = tokenStr.split(' ')
    token = bearerToken[1]
    # algorithms=['HS256']
    print("token: ", token)
    if bearerToken[0] != "Bearer":
        return JsonResponse({'Warning': 'Token is invalid Berear!'}, status=status.HTTP_200_OK)
    
    try:
        # payload = jwt.decode(token, settings.SECRET_KEY_TOKEN, algorithms=['HS256'])
        decoded_payload = jwt.decode(token, settings.SECRET_KEY_TOKEN, algorithms=["HS256"])
        # decodedPayload = jwt.decode(token,options={"verify_signature": False})
        print("tokeni parsi: ", decoded_payload)
        userType = decoded_payload['Usertype']
        print("tokende usertype: ", userType)
    except:
        return JsonResponse({'Warning': 'Token is invalid! decode'}, status=status.HTTP_200_OK)
    if userType != '2':
        return JsonResponse({'Warning': 'You have not permission to create courier!'}, status=status.HTTP_200_OK)    
    # print("Cook create-da request.data", cook_data)
    courier_serializer = ShortCourierCreateSerializer(data=cook_data)
    # print("Cook serializeri cap edirem", cook_serializer)
    # raise_exception=True
    if courier_serializer.is_valid():
        courier_serializer.save()
        # return JsonResponse({'Cook': cook_serializer}, status=status.HTTP_200_OK)
        print("Ser Data id", courier_serializer.data['id'])
        # return JsonResponse(cook_serializer.data)
        return JsonResponse({'Message': f"Courier with id {courier_serializer.data['id']} is successfully created!"}, status=status.HTTP_200_OK) 
        # return JsonResponse({'Message': 'The cook is successfully created!'}, status=status.HTTP_200_OK)
    else:
        print(courier_serializer.errors)
        return JsonResponse(courier_serializer.errors, status=status.HTTP_200_OK)
        # return JsonResponse(cook_serializer.errors, status=status.HTTP_200_OK)
        # return JsonResponse({'Warning': 'Request data is invalid'}, status=status.HTTP_200_OK)



class CourierAPIView(RetrieveUpdateDestroyAPIView):
    # authentication_classes = []
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Courier.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = CourierSerializer

    def put(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'Only courier himself can update the courier!'}, status=status.HTTP_403_FORBIDDEN)
        if not courier:
            return JsonResponse (data=[], status=200, safe=False)
        serializer = CourierSerializer(data=self.request.data,
                                       instance=courier, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False)

    def delete(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'Only courier himself can delete the courier!'}, status=status.HTTP_403_FORBIDDEN)
        if not courier:
            return JsonResponse (data=[], status=200, safe=False)
        serializer = CourierSerializer(courier)
        courier.delete()
        print('deleteddd')
        print(serializer.data)
        # return JsonResponse(data="Courier is deleted successfully!", safe=False)
        return JsonResponse({'message': 'Courier is deleted successfully!'}, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'Only courier himself can update the courier!!'}, status=status.HTTP_200_OK)
        serializer = CourierSerializer(data=self.request.data, instance=courier, 
                                    context={'request': self.request}, partial=True) # set partial=True to update a data partially
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse( data=serializer.data, safe=False)
        return JsonResponse( data="Wrong parameters")



class DeliveryAreasAPIView(ListAPIView):
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