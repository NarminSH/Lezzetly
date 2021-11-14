from django.conf import settings
from django.http.response import JsonResponse
import jwt
from rest_framework import status

def checkToken(tokenStr):
    respMessage = None
    if tokenStr is None:
        respMessage = {'warning': 'You are unauthorized, please login.'}
    else:
        bearerToken = tokenStr.split(' ')
        token = bearerToken[1]
        
        if bearerToken[0] != "Bearer":
            respMessage = {'warning': 'Token is not Berear token!'}
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY_TOKEN, algorithms=["HS256"])
            secureIss = "go-auth-system"
            if "iss" not in decoded_payload or decoded_payload["iss"] != secureIss:
                respMessage = {'warning': 'You have not permission, not secure token!'}
        except jwt.ExpiredSignatureError:
            respMessage = {'warning': 'Token is expired. Please login again!'}
        except jwt.InvalidTokenError:
            respMessage = {'warning': 'Token is invalid!'}
    if respMessage != None:
        return respMessage
    return decoded_payload
    
