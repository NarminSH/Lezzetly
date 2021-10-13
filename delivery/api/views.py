from django.http import request
from django.http.response import Http404, JsonResponse
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from cooks.models import Cook
from delivery.api.serializers import CourierSerializer, DeliveryAreaSerializer
from delivery.models import Courier, DeliveryArea
from orders.api.serializers import OrderFullSerializer
from orders.models import Order


class CouriersAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # queryset = Courier.objects.filter(is_available=True, transport__isnull=False, 
    #                         rating__isnull=False, work_experience__isnull=False, deliveryArea__isnull=False )
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    search_fields = ['deliveryArea__delivery_area']
    filter_backends = (filters.SearchFilter,)



class CourierOrdersAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):
            item = Order.objects.filter(courier=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = OrderFullSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CourierAreasAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    # queryset = Order.objects.all()


    def get(self, *args, **kwargs):
            item = Courier.objects.filter(courier=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = OrderFullSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CourierAPIView(RetrieveUpdateDestroyAPIView):
    # authentication_classes = []
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Courier.objects.all()
    lookup_url_kwarg = 'pk'
    serializer_class = CourierSerializer

    def put(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'You do not have permissions to update the user!'}, status=status.HTTP_200_OK)
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
            return JsonResponse({'message': 'You do not have permissions to delete the user!'}, status=status.HTTP_200_OK)
        if not courier:
            raise Http404
        serializer = CourierSerializer(courier)
        courier.delete()
        print('deleteddd')
        print(serializer.data)
        # return JsonResponse(data="Courier is deleted successfully!", safe=False)
        return JsonResponse({'message': 'deleted courier!'}, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        courier = Courier.objects.filter(pk=kwargs.get('pk')).first()
        if courier != self.request.user:
            return JsonResponse({'message': 'You do not have permissions to update the user!'}, status=status.HTTP_200_OK)
        serializer = CourierSerializer(data=self.request.data, instance=courier, 
                                    context={'request': self.request}, partial=True) # set partial=True to update a data partially
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse( data=serializer.data, safe=False)
        return JsonResponse( data="Wrong parameters")



class DeliveryAreasAPIView(ListCreateAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DeliveryArea.objects.all()
    serializer_class = DeliveryAreaSerializer 

