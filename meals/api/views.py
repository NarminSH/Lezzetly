from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import filters

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .serializers import MealSerializer
from ..models import Meal

@api_view(['GET'])
def mealsApiOverviews(request):
    api_urls = {
        'List of meals': '/meals',
        'Meals detail': '/meals/<str:pk>',
        'Create meal': '/meal-create',
        'Update meal': '/meal-update/<str:pk>',
        'Delete meal': '/meal-delete/<str:pk>',
        # 'List of categories': '/categories'
    }
    return Response(api_urls)

class MealAPIView(generics.ListCreateAPIView):
    search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title']
    filter_backends = (filters.SearchFilter,)
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


@api_view(['GET'])
def mealDetail(request, pk):
    meal = Meal.objects.get(id=pk)
    serializer = MealSerializer(meal, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def mealCreate(request):
    serializer = MealSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def mealUpdate(request, pk):
    meal = Meal.objects.get(id=pk)
    serializer = MealSerializer(instance=meal, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def mealDelete(request, pk):
    meal = Meal.objects.get(id=pk)
    meal.delete()
    return Response("Successfully deleted!")
