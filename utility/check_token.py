from django.conf import settings
from django.http.response import JsonResponse
import jwt
from rest_framework import status

def checkToken(tokenStr):
    respMessage = None
    bearerToken = tokenStr.split(' ')
    token = bearerToken[1]
    
    if bearerToken[0] != "Bearer":
        respMessage = {'warning': 'Token is not Berear token!'}
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY_TOKEN, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        respMessage = {'warning': 'Token is expired. Please login again!'}
    except jwt.InvalidTokenError:
        respMessage = {'warning': 'Token is invalid!'}
    if respMessage != None:
        return respMessage
    return decoded_payload
    
