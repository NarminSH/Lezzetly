from django.urls import path
from users.api.views import RegisterAPIView, LoginAPIView, AuthUserAPIView



app_name = 'users_api'

urlpatterns = [
    # path('users/', UsersAPIView.as_view(), name='locations'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', AuthUserAPIView.as_view(), name='user'),
]