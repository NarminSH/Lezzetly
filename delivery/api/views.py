# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
# from delivery.api.serializers import CourierSerializer
# from delivery.models import Courier


# class CouriersAPIView(ListCreateAPIView):
#     authentication_classes = []
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Courier.objects.filter(is_active=True)
#     serializer_class = CourierSerializer


# class CourierAPIView(RetrieveUpdateDestroyAPIView):
