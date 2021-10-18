
from rest_framework import permissions
from django.http.response import Http404, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
from rest_framework.generics import  ListAPIView, ListCreateAPIView
from cooks.api.serializers import CookListSerializer, CookSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer
from cooks.models import Cook, Recommendation, Resume
from users.api.serializers import RegisterSerializer
from orders.api.serializers import OrderFullSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal



class CooksAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Cook.objects.filter(is_available=True)
    serializer_class = CookListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return super(CooksAPIView, self).get_serializer_class()



test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual parametrs", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('Get information about single cook with id', CookSerializer)
put_response = openapi.Response('Change information about single cook with id', CookSerializer)


# 'method' can be used to customize a single HTTP method of a view
@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['put', 'PATCH', 'DELETE'], request_body=CookSerializer, responses={200: put_response})
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
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

    elif request.method == 'PUT': 
        if request.user == cook:
            cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            cook_serializer = CookSerializer(cook, data=cook_data) 
            if cook_serializer.is_valid(raise_exception=True): 
                cook_serializer.save() 
                return JsonResponse(cook_serializer.data) 
            return JsonResponse(cook_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        return JsonResponse({'message': 'You have no rights to change this cook!'}, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'PATCH': 
        if request.user == cook:
            cook_data = JSONParser().parse(request) # don't forget you are able to send only json data
            cook_serializer = CookSerializer(cook, data=cook_data, partial=True) 
            if cook_serializer.is_valid(raise_exception=True): 
                cook_serializer.save() 
                return JsonResponse(cook_serializer.data) 
            return JsonResponse(cook_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        return JsonResponse({'message': 'You have no rights to change this cook!'}, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'DELETE':
        if request.user == cook:
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
                    return JsonResponse({'message': 'You have ongoing order!'}, status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({'message': 'You have no rights to delete the cook!'}, status=status.HTTP_403_FORBIDDEN)   #changed status fromm 200 to 403
    



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
                raise Http404
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
                raise Http404
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
                raise Http404
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
                    raise Http404
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