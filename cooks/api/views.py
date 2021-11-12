
from rest_framework import permissions
from django.http.response import Http404, JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser 
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
from rest_framework.generics import  ListAPIView, ListCreateAPIView
from cooks.api.serializers import CookCreateSerializer, CookListSerializer, CookSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer, ShortCookCreateSerializer
from cooks.models import Cook, Recommendation, Resume, Client
from users.api.serializers import RegisterSerializer
from orders.api.serializers import OrderFullSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal
import jwt
from django.conf import settings

from utility.check_token import checkToken


# class CooksAPIView(ListCreateAPIView):
class CooksAPIView(generics.ListAPIView):
    # authentication_classes = []
    # permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    # queryset = Meal.objects.filter(is_active=True)
    # serializer_class = MealSerializer

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Cook.objects.filter(is_available=True)
    serializer_class = CookListSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return RegisterSerializer
    #     return super(CooksAPIView, self).get_serializer_class()

# authentication_classes = []
# permission_classes = []
# @permission_classes([AllowAny])

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@swagger_auto_schema(method = 'POST',request_body=ShortCookCreateSerializer)
@parser_classes([JSONParser, MultiPartParser])
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def cookCreate(request):
    print("****************")
    print("cook create-e daxil oldu")
    # client1 = Client.objects.filter(id = 1).first()
    # print(client1, "cleint 1")
    # try: 
    #     client1 = Client.objects.get(id = 1) 
    # except: 
    #     client1 = None
        # return JsonResponse({'Warning': 'You have not permission to create cook with this token!'}, status=status.HTTP_200_OK)
    cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
    
    if claimsOrMessage['Usertype'] != '1':
        return JsonResponse({'Warning': 'You have not permission to create cook!'}, status=status.HTTP_200_OK)    
    cook_serializer = ShortCookCreateSerializer(data=cook_data)
    
    try:
        currentCook = Cook.objects.get(username = claimsOrMessage['Username'])
        return JsonResponse({'Warning': f'The cook with this username({currentCook.username}) already exists!'}, status=status.HTTP_200_OK)
    except Cook.DoesNotExist: 
        if cook_serializer.is_valid():
            cook_serializer.save(username = claimsOrMessage['Username'], user_type = claimsOrMessage['Usertype'])

            return JsonResponse({'Message': f"Cook with id {cook_serializer.data['id']} is successfully created! and Client: "}, status=status.HTTP_200_OK) 
            # return JsonResponse({'Message': 'The cook is successfully created!'}, status=status.HTTP_200_OK)
        elif 'email' in cook_serializer.errors and 'username'in cook_serializer.errors:
            print(cook_serializer.errors)
            return JsonResponse({'warning': 'cook with this username and email already exists!'}, status=status.HTTP_200_OK)
        elif 'email' in cook_serializer.errors:
            return JsonResponse({'warning': 'cook with this email already exists!'}, status=status.HTTP_200_OK)
        elif 'username' in cook_serializer.errors:
            return JsonResponse({'warning': 'cook with this username already exists!'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(cook_serializer.errors, status=status.HTTP_200_OK)


test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual parametrs", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('Get information about single cook with id', CookSerializer)
put_response = openapi.Response('Change information about single cook with id', CookSerializer)

# 'method' can be used to customize a single HTTP method of a view
@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['put', 'PATCH', 'DELETE'], request_body=CookSerializer, responses={200: put_response})
@parser_classes([JSONParser, MultiPartParser])
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
# @authentication_classes([])  # if enable this decorator user will always be anonymous and without this decorator user has to login even for get method
# @permission_classes([AllowAny])
@authentication_classes([])
@permission_classes([])
def cook_detail(request, pk):
    print("Daxil oldu cook_detail-a")
    try: 
        cook = Cook.objects.get(pk=pk) 
    except Cook.DoesNotExist: 
        return JsonResponse({'Warning': 'The cook does not exist'}, status=status.HTTP_200_OK) 
    cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
    if request.method == 'GET':
        if claimsOrMessage['Username'] == cook.username and claimsOrMessage['Usertype'] == "1":  
            cook_serializer = CookSerializer(cook)
            return JsonResponse(cook_serializer.data)
        else:
            return JsonResponse({'Warning': 'You have not permission to get this cook info!'}, status=status.HTTP_200_OK) 
        

    elif request.method == 'PUT': 
        if claimsOrMessage['Username'] == cook.username and claimsOrMessage['Usertype'] == "1":
            # cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            if 'username' in cook_data:
                if cook_data['username'] != claimsOrMessage['Username']:
                    return JsonResponse({'Warning': 'You can not change username!'}, status=status.HTTP_200_OK)
            if 'user_type' in cook_data:
                if cook_data['user_type'] != claimsOrMessage['Usertype']:
                    return JsonResponse({'Warning': 'You can not change user_type!'}, status=status.HTTP_200_OK)
            cook_serializer = CookSerializer(cook, data=cook_data) 
            if cook_serializer.is_valid():
                cook_serializer.save() 
                return JsonResponse(cook_serializer.data)
            elif 'email' in cook_serializer.errors:
                return JsonResponse({'warning': 'Courier with this email address already exists.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(cook_serializer.errors, status=status.HTTP_200_OK) 
        return JsonResponse({'warning': 'You have no rights to change this cook!'}, status=status.HTTP_200_OK)


    elif request.method == 'PATCH': 
        if claimsOrMessage['Username'] == cook.username and claimsOrMessage['Usertype'] == "1":
            # cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            if 'username' in cook_data:
                if cook_data['username'] != claimsOrMessage['Username']:
                    return JsonResponse({'Warning': 'You can not change username!'}, status=status.HTTP_200_OK)
            if 'user_type' in cook_data:
                if cook_data['user_type'] != claimsOrMessage['Usertype']:
                    return JsonResponse({'Warning': 'You can not change user_type!'}, status=status.HTTP_200_OK)
            cook_serializer = CookSerializer(cook, data=cook_data, partial=True) 
            if cook_serializer.is_valid(): 
                cook_serializer.save()
                return JsonResponse(cook_serializer.data)
            elif 'email' in cook_serializer.errors:
                return JsonResponse({'warning': 'Courier with this email address already exists.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(cook_serializer.errors, status=status.HTTP_200_OK) 
        return JsonResponse({'warning': 'You have no rights to change this cook!'}, status=status.HTTP_200_OK)


    elif request.method == 'DELETE':
        if claimsOrMessage['Username'] == cook.username and claimsOrMessage['Usertype'] == "1":
            all_orders = cook.orders.all()
            ongoing_orders = 0
            if all_orders:
                for order in all_orders:
                    if order.complete == False:
                        ongoing_orders += 1
                if ongoing_orders == 0:
                    cook.delete()   
                    return JsonResponse({'message': 'The cook was deleted successfully!'}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'warning': 'You have ongoing order!'}, status=status.HTTP_200_OK)
        return JsonResponse({'warning': 'You have no rights to delete the cook!'}, status=status.HTTP_200_OK)   #changed status fromm 200 to 403
    

class RecommendationsAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationListSerializer


class CookRecommendationsAPIView(ListCreateAPIView):
    # authentication_classes = []
    permission_classes = [permissions.AllowAny]

    serializer_class = RecommendationSerializer
    queryset = Recommendation.objects.all()

    def get(self, *args, **kwargs):
            item = Recommendation.objects.filter(cook=kwargs.get('pk'))
            if not item:
                return JsonResponse (data=[], status=200, safe=False)
            serializer = RecommendationSerializer(
                item, many=True, context={'request': self.request}, exclude=['cook'])
            return JsonResponse(data=serializer.data, safe=False)

    def post(self, *args, **kwargs):
        recommendation_data = self.request.data
        if self.request.user.id == kwargs.get('pk'): 
            serializer = RecommendationSerializer(data=recommendation_data, context={
                                            'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['cook']= self.request.user
            serializer.save()
            return JsonResponse(data=serializer.data, safe=False, status=201)
        return JsonResponse (data="You do not have permissions to give recommendations to the cook!", status=403, safe=False) #changed status to 403


class CookResumesAPIView(ListCreateAPIView):
    # authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

    def get(self, *args, **kwargs):
            item = Resume.objects.filter(cook=kwargs.get('pk'))
            if not item:
                return JsonResponse (data=[], status=200, safe=False)
            serializer = ResumeSerializer(
                item, many=True, context={'request': self.request}, exclude=['cook'])
            return JsonResponse(data=serializer.data, safe=False)

    
    def post(self, *args, **kwargs):
        resume_data = self.request.data
        if self.request.user.id == kwargs.get('pk'): 
            serializer = ResumeSerializer(data=resume_data, context={
                                            'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['cook']= self.request.user
            serializer.save()
            return JsonResponse(data=serializer.data, safe=False, status=201)
        return JsonResponse (data="You do not have permissions to create a resume for the cook!", status=403, safe=False)

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@swagger_auto_schema(method = 'POST',request_body=ShortCookCreateSerializer)
@parser_classes([JSONParser, MultiPartParser])
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def logout(request):
    
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)

    bearerToken = tokenStr.split(' ')
    token = bearerToken[1]

    token_serializer = ShortCookCreateSerializer()
    token_serializer.save(token=token)
    return JsonResponse({'message': 'Token added to blacklist!'}, status=status.HTTP_200_OK)


class ResumesAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Resume.objects.all()
    serializer_class = ResumeListSerializer

class CookMealsAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = MealSerializer
    queryset = Meal.objects.all()


    def get(self, *args, **kwargs):
            item = Meal.objects.filter(cook=kwargs.get('pk'))
            if not item:
                return JsonResponse (data=[], status=200, safe=False)
            serializer = MealSerializer(
                item, many=True, context={'request': self.request}, exclude=["cook", ])
            return JsonResponse(data=serializer.data, safe=False)


class CookOrdersAPIView(ListAPIView):   #changed all api views to generic ones bcz of swagger documentation
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()
    

    def get(self, *args, **kwargs):
            item = Order.objects.filter(cook=kwargs.get('pk'))
            if self.request.user.id == kwargs.get('pk'):
                if not item:
                    return JsonResponse (data=[], status=200, safe=False)
                serializer = OrderFullSerializer(
                    item, many=True, context={'request': self.request}, exclude=['cook'])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse(data="You don't own permissions for this action", safe=False, status=403)



class CookActiveOrdersAPIView(ListAPIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()


    def get(self, *args, **kwargs):
            item = Order.objects.filter(cook=kwargs.get('pk'), complete=False)
            print(self.request.user)
            if self.request.user.id == kwargs.get('pk'): 
                if not item:
                    return JsonResponse (data=[], status=200, safe=False)
                serializer = OrderFullSerializer(
                    item, many=True, context={'request': self.request}, exclude=["cook"])
                return JsonResponse(data=serializer.data, safe=False)
            return JsonResponse (data="You do not have permissions to look at other cooks' orders!", status=403, safe=False)