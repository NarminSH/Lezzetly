from django.contrib.auth import authenticate
from rest_framework import permissions
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import authentication, permissions, serializers
from lezzetly.settings import SECRET_KEY
from users.models import User
import os
from users.api.serializers import RegisterSerializer, LoginSerializer


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    model = User
    
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        register_data = self.request.data
        serializer = RegisterSerializer(data=register_data, context={
                                        'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False, status=201)


class LoginAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            # print("user", user.token)
            serializer = self.serializer_class(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
