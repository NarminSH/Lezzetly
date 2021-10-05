from rest_framework import permissions
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from users.models import User
from users.api.serializers import RegisterSerializer, UserDetailSerializer


class RegisterAPIView(CreateAPIView):

    model = User
    # permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        register_data = self.request.data
        serializer = RegisterSerializer(data=register_data, context={
                                        'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, safe=False, status=201)


class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(data=request.data,
                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserDetailSerializer(user)
        return Response(user_serializer.data, status=200)