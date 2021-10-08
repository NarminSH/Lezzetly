from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from cooks.models import Cook
from delivery.api.serializers import CourierSerializer
from delivery.models import Courier


class CouriersAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Courier.objects.filter(is_active=True)
    serializer_class = CourierSerializer


class CooknearCouriersAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    cook_service_places = Cook.objects.all().order_by('-created_at')[:3]
    serializer_class = CourierSerializer
    queryset = CourierSerializer
    for cook_service_place in cook_service_places:
        cook_place = cook_service_place.service_place
        # print(cook_place)
    # couriers = Courier.objects.filter(service_place  )



