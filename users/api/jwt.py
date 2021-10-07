from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from cooks.models import Cook
from users.models import User
import os
import jwt


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid!')
        token = auth_token[1]

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algoritms="HS256")
            email = payload['email']
            user = Cook.objects.get(email=email)
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired, login again!')
        except jwt.DecodeError as ex:
            print('asadfghjhgf')
            raise exceptions.AuthenticationFailed(
                'Token is invalid!')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No such user!')
                
        return (user, token)
    # return super().authenticate(request)