from rest_framework import permissions
from django.http.response import Http404, JsonResponse
from rest_framework.generics import  ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from cooks.api.serializers import CookListSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer
from cooks.models import Cook, Recommendation, Resume
from users.api.serializers import RegisterSerializer
from orders.api.serializers import OrderListSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal


class CooksAPIView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Cook.objects.filter(is_active=True)
    serializer_class = CookListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return super(CooksAPIView, self).get_serializer_class()


class CookAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CookListSerializer
    queryset = Cook.objects.filter(is_active=True)
    lookup_url_kwarg = 'pk'



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

