
from django.contrib.auth.models import AnonymousUser
from django.http import request
from rest_framework import permissions
from django.http.response import Http404, JsonResponse
from rest_framework.generics import  ListAPIView, ListCreateAPIView
from cooks.api.serializers import CookListSerializer, CookSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer
from cooks.models import Cook, Recommendation, Resume
from users.api.serializers import RegisterSerializer
from orders.api.serializers import OrderFullSerializer, OrderListSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status


class CooksAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Cook.objects.filter(is_available=True)
    serializer_class = CookListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return super(CooksAPIView, self).get_serializer_class()




@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([])  # if enable this decorator user will always be anonymous and without this decorator user has to login even for get method
@permission_classes([AllowAny])
def cook_detail(request, pk):
    try: 
        cook = Cook.objects.get(pk=pk) 
    except Cook.DoesNotExist: 
        return JsonResponse({'message': 'The cook does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        if request.user.user_type == '2' or request.user.user_type == '1':  
            cook_serializer = CookSerializer(cook)
            return JsonResponse(cook_serializer.data)
        cook_serializer = CookListSerializer(cook) 
        return JsonResponse(cook_serializer.data) 

    elif request.method == 'PUT' and request.user == cook: 
        cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
        cook_serializer = CookSerializer(cook, data=cook_data) 
        if cook_serializer.is_valid(raise_exception=True): 
            cook_serializer.save() 
            return JsonResponse(cook_serializer.data) 
        return JsonResponse(cook_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        if request.user == cook:
            print(request.user)
            print(cook)
            all_orders = cook.orders.all()
            ongoing_orders = 0
            print(all_orders)
            if all_orders:
                for order in all_orders:
                    if order.complete == False:
                        ongoing_orders += 1
                if ongoing_orders == 0:
                    cook.delete()   
                    print('deletedddddddd')       
                    return JsonResponse({'message': 'The cook was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({'message': 'You have ongoing order!'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'You have no rights to delete the cook!'}, status=status.HTTP_204_NO_CONTENT)
    



class RecommendationsAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecommendationSerializer
        return super(RecommendationsAPIView, self).get_serializer_class()



class CookRecommendationsAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    serializer_class = RecommendationSerializer
    queryset = Recommendation.objects.all()

    def get(self, *args, **kwargs):
            item = Recommendation.objects.filter(cook=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = RecommendationSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class ResumesAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Resume.objects.all()
    serializer_class = ResumeListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResumeSerializer
        return super(ResumesAPIView, self).get_serializer_class()


class CookResumesAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

    def get(self, *args, **kwargs):
            item = Resume.objects.filter(cook=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = ResumeSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookMealsAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = MealSerializer
    queryset = Meal.objects.all()


    def get(self, *args, **kwargs):
            item = Meal.objects.filter(cook=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = MealSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookOrdersAPIView(ListAPIView):   #changed all api views to generic ones bcz of swagger documentation
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderFullSerializer
    queryset = Order.objects.all()
    

    def get(self, *args, **kwargs):
            item = Order.objects.filter(cook=kwargs.get('pk'))
            if not item:
                raise Http404
            serializer = OrderFullSerializer(
                item, many=True, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)

