from orders.models import OrderItem
from orders.api.views import order_create
from django.urls import path
from . import views
app_name = 'orders_api'

urlpatterns = [
    # path('orders/', OrdersAPIView.as_view(), name='orders'),
    # path('orders/<int:pk>',OrderAPIView.as_view(), name='order'),
    # path('orders/completed',OrdersCompleteAPIView.as_view(), name='orders-complete'),
    # path('orderitem/<int:pk>', OrderItemAPIView.as_view(), name='orderitem'),
    path('order-create/', order_create, name='create-order'),
    path('orders/', views.OrderAPIView.as_view(), name='order-list'),
    path("orders/<str:pk>/", views.order_detail),
    path("add-courier/<str:pk>/", views.add_courier_to_order),
    path("complete-order/<str:pk>/", views.complete_order),
    path("reject-order/<str:pk>/", views.reject_order),
    path("orderitems/", views.OrderItemAPIView.as_view())
]