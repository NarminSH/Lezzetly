from os import name
from django.urls.conf import path
from delivery.api.views import CouriersAPIView


urlpatterns = [
    path('couriers/', CouriersAPIView.as_view(), name='couriers'),
    # path('couriers/<int:pk>', CooknearCouriersAPIView.as_view(), name='cooknearcouriers')
]