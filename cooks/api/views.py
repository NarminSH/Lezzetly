from orders.api.serializers import OrderListSerializer, OrderSerializer
from orders.models import Order
from meals.api.serializers import MealSerializer
from meals.models import Meal
from django.http.response import Http404, JsonResponse
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from cooks.api.serializers import CookListSerializer, RecommendationListSerializer, RecommendationSerializer, ResumeListSerializer, ResumeSerializer
from cooks.models import Cook, Recommendation, Resume


class CooksAPIView(ListCreateAPIView):
    queryset = Cook.objects.filter(is_active=True)
    serializer_class = CookListSerializer


class CookAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CookListSerializer
    queryset = Cook.objects.filter(is_active=True)
    lookup_url_kwarg = 'pk'



class RecommendationsAPIView(ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecommendationSerializer
        return super(RecommendationsAPIView, self).get_serializer_class()



class CookRecommendationsAPIView(APIView):
    serializer_class = RecommendationSerializer

    def get(self, *args, **kwargs):
            item = Recommendation.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = RecommendationSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class ResumesAPIView(ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResumeSerializer
        return super(ResumesAPIView, self).get_serializer_class()


class CookResumesAPIView(APIView):
    def get(self, *args, **kwargs):
            item = Resume.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = ResumeSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookMealsAPIView(APIView):
    def get(self, *args, **kwargs):
            item = Meal.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = MealSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)


class CookOrdersAPIView(APIView):

    def get(self, *args, **kwargs):
            cook_data = self.request.data
            print(cook_data)
            item = Order.objects.filter(cook=kwargs.get('pk')).first()
            if not item:
                raise Http404
            serializer = OrderListSerializer(
                item, context={'request': self.request})
            return JsonResponse(data=serializer.data, safe=False)
