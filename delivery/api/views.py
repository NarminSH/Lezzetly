from rest_framework import permissions
from delivery.models import Courier
from django.http.response import Http404, JsonResponse
from rest_framework.generics import  ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from delivery.api.serializers import CourierListSerializer
from delivery.models import Courier, DeliveryArea
from users.api.serializers import RegisterSerializer


class CouriersAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Courier.objects.filter(is_available=True)
    serializer_class = CourierListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return super(CouriersAPIView, self).get_serializer_class()
