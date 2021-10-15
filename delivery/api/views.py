from django.contrib.auth.models import AnonymousUser
from django.http import request
from django.http.response import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import filters, serializers, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticatedOrReadOnly
from cooks.models import Cook
from delivery.api.serializers import CourierSerializer, DeliveryAreaPriceListSerializer, DeliveryAreaPriceSerializer, DeliveryAreaSerializer
from delivery.models import Courier, DeliveryArea, DeliveryPrice
from orders.api.serializers import OrderFullSerializer
from orders.models import Order


class CouriersAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # queryset = Courier.objects.filter(is_available=True, transport__isnull=False, 
    #                         rating__isnull=False, work_experience__isnull=False, deliveryArea__isnull=False )
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer




class CourierOrdersAPIView(ListAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()

    # serializer_class_Order = OrderFullSerializer
    # serializer_class_delivery = DeliveryAreaPriceListSerializer
    

    # def get_queryset_Order(self):
    #     order =  Order.objects.filter(courier=self.kwargs.get('pk'), complete=True)
    #     return order
    

    # def get_queryset_delivery(self):
    #     courier = DeliveryPrice.objects.filter(courier=self.kwargs.get('pk'))
    #     print(courier.delivery_areas, 'dslcmlksmdlkcmslkdmc')
    #     return courier

    # def list(self, request, *args, **kwargs):
    #     delivery = self.serializer_class_delivery(self.get_queryset_delivery(), many=True, context={'request': self.request})
    #     order = self.serializer_class_Order(self.get_queryset_Order(), many=True, context={'request': self.request})

    #     return Response({
    #         "**ORDER**": order.data,
    #         "**DELIVERY**": delivery.data
    #     })


    def get(self, *args, **kwargs):
            item = Order.objects.filter(courier=kwargs.get('pk'), complete=True)
            if self.request.user.id != kwargs.get('pk'): 
                if not item:
                    raise Http404
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
            if self.request.user.id == kwargs.get('pk'): 
                if not item:
                    raise Http404
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
                raise Http404
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
            raise Http404
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
            raise Http404
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
            raise Http404
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
            raise Http404
        delivery_area.delete()
        return JsonResponse({'message': 'Delivery area is deleted successfully!'}, status=status.HTTP_200_OK)



class CouriersDeliveryAreasAPIView(ListAPIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = DeliveryPrice.objects.all()
    serializer_class = DeliveryAreaPriceListSerializer