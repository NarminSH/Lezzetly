from django.urls import path
from users.api.views import AuthUserAPIView, RegisterAPIView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users_api'

urlpatterns = [
    # path('users/', UsersAPIView.as_view(), name='locations'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    # path('login/', LoginAPIView .as_view(), name='login'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', AuthUserAPIView.as_view(), name='user'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
