from django.http.response import Http404, JsonResponse
from rest_framework import filters
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
    queryset = Courier.objects.filter(is_available=True, transport__isnull=False, 
                            rating__isnull=False, work_experience__isnull=False, deliveryArea__isnull=False )
    serializer_class = CourierSerializer
    search_fields = ['deliveryArea']
    filter_backends = (filters.SearchFilter,)




class CourierOrdersAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    # queryset = Order.objects.all()


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

class DeliveryAreasAPIView(ListCreateAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DeliveryArea.objects.all()
    serializer_class = DeliveryAreaSerializer 

