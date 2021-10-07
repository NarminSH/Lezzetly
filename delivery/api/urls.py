from django.urls.conf import path
from delivery.api.views import CouriersAPIView


urlpatterns = [
    path('couriers/', CouriersAPIView.as_view(), name='cooks'),
]