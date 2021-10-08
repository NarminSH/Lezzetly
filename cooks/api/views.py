
from rest_framework import permissions
from django.http.response import Http404, JsonResponse
from rest_framework.generics import  ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from cooks.api.serializers import CookListSerializer, CookSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer
from cooks.models import Cook, Recommendation, Resume
from users.api.serializers import RegisterSerializer
from orders.api.serializers import OrderListSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
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
# @permission_classes([IsAuthenticatedOrReadOnly])
def cook_detail(request, pk):
    try: 
        cook = Cook.objects.get(pk=pk) 
    except Cook.DoesNotExist: 
        return JsonResponse({'message': 'The cook does not exist'}, status=status.HTTP_404_NOT_FOUND) 


    if request.method == 'GET' and request.user.user_type == '2' :
        cook_serializer = CookSerializer(cook)
        return JsonResponse(cook_serializer.data)

    elif request.method == 'GET': 
        cook_serializer = CookListSerializer(cook) 
        return JsonResponse(cook_serializer.data) 

    elif request.method == 'PUT': 
        cook_data = JSONParser().parse(request) 
        cook_serializer = CookSerializer(cook, data=cook_data) 
        if cook_serializer.is_valid(): 
            cook_serializer.save() 
            return JsonResponse(cook_serializer.data) 
        return JsonResponse(cook_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE' and request.user != cook :
        all_orders = cook.orders.all()
        for order in all_orders:
            if order.complete == False:
                not_completed_orders = True
        if not not_completed_orders:
            cook.delete()   
            print('deletedddddddd')       
            return JsonResponse({'message': 'The cook was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
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
            item = Recommendation.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = RecommendationSerializer(
                item, context={'request': self.request})
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
            item = Resume.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = ResumeSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookMealsAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = MealSerializer
    queryset = Meal.objects.all()


    def get(self, *args, **kwargs):
            item = Meal.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = MealSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookOrdersAPIView(ListAPIView):   #changed all api views to generic ones bcz of swagger documentation
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    

    def get(self, *args, **kwargs):
            item = Order.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = OrderListSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)

