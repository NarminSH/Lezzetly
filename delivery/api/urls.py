from os import name
from django.urls.conf import path
from delivery.api.views import CourierAPIView, CourierActiveOrdersAPIView, CourierAreasAPIView, CourierOrdersAPIView, CouriersAPIView, DeliveryAreasAPIView


urlpatterns = [
    path('couriers/', CouriersAPIView.as_view(), name='couriers'),
    path('couriers/<int:pk>', CourierAPIView.as_view(), name='courier'),
    path('couriers/<int:pk>/orders/', CourierOrdersAPIView.as_view(), name='courierorders'),
    path('couriers/<int:pk>/activeorders/', CourierActiveOrdersAPIView.as_view(), name='courieractiveorders'),
    path('deliveryareas/', DeliveryAreasAPIView.as_view(), name='deliveryareas'),
    path('couriers/<int:pk>/deliveryareas', CourierAreasAPIView.as_view(), name='courierareas'),
    # path('couriers/<int:pk>/active-orders', CourierOrdersAPIView.as_view(), name='courierorders'),
]