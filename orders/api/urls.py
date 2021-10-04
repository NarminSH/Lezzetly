from orders.models import OrderItem
from orders.api.views import OrderAPIView, OrderItemAPIView, OrdersAPIView, OrdersCompleteAPIView
from django.urls import path
app_name = 'orders_api'



urlpatterns = [
    path('orders/', OrdersAPIView.as_view(), name='orders'),
    path('orders/<int:pk>',OrderAPIView.as_view(), name='order'),
    path('orders/completed',OrdersCompleteAPIView.as_view(), name='orders-complete'),
    path('orderitem/<int:pk>', OrderItemAPIView.as_view(), name='orderitem'),

]