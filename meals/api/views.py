from .filters import MealFilter
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import filters
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CategoryCustomSerializer, MealSerializer, MealCreatSerializer, CategoryUpdateSerializer
from ..models import Category, Meal

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
@api_view(['GET'])
def mealsApiOverviews(request):
    api_urls = {
        'List of meals': '/meals',
        'Meals detail': '/meals/<str:pk>',
        'Create meal': '/meal-create',
        'Update meal': '/meals/<str:pk>',
        'Delete meal': '/meals/<str:pk>',
        'list of categories': '/categories',
        'category detail': '/categories/<str:pk>',
        'Create category': '/categories',
        'Update category': '/categories/<str:pk>',
        'Delete category': '/categories/<str:pk>',
    }
    return Response(api_urls)

class MealAPIView(generics.ListAPIView):
    authentication_classes = []
    search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title']
    filter_backends = (filters.SearchFilter,)
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

# Api for  get all meals and for search
# for search - meals/?search=lunch 
# class MealAPIView(generics.ListCreateAPIView):
#     model = Meal
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return MealCreatSerializer
#         return MealSerializer
#     search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title']
#     filter_backends = (filters.SearchFilter,)
#     def get_queryset(self):
#         return Meal.objects.filter(is_active=True)
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         item = Meal.objects.create(
#             title=serializer.data['title'],
#             price=serializer.data['price'],
#             stock_quantity=serializer.data['stock_quantity'],
#             is_active=serializer.data['is_active'],
#             cook=serializer.data['cook'],
#             category=serializer.data['category'],
#             ingredients=serializer.data['ingredients'],
#             mealoption=serializer.data['mealoption']
#             )
#         result = MealSerializer(item)
#         return Response(result.data, status=status.HTTP_201_CREATED)
    # queryset = Meal.objects.filter(is_active=True)
    # serializer_class = MealSerializer


# create new meals,
# delete all meals, now in comment
@api_view(['POST', 'DELETE'])
def meal_list(request):
    # if request.method == 'GET':
    #     queryset = Meal.objects.filter(is_active=True)
        
    #     # title = request.query_params.get('search', None)
    #     # if title is not None:
    #     #     meals = meals.filter(title__icontains=title, price__icontains=title)
        
    #     filterset = MealFilter(request.GET, queryset=queryset)
    #     if filterset.is_valid():
    #         queryset = filterset.qs


    #     meals_serializer = MealSerializer(queryset, many=True)
    #     return JsonResponse(meals_serializer.data, safe=False)
    #     # 'safe=False' for objects serialization
 
    if request.method == 'POST':
        meal_data = JSONParser().parse(request)
        meal_serializer = MealCreatSerializer(data=meal_data)
        if meal_serializer.is_valid():
            meal_serializer.save()
            return JsonResponse(meal_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

# get single meal
# update meal
# delete meal 
@api_view(['GET', 'PUT', 'DELETE'])
def meal_detail(request, pk):
    try: 
        meal = Meal.objects.get(pk=pk) 
    except Meal.DoesNotExist: 
        return JsonResponse({'message': 'The meal does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        meal_serializer = MealSerializer(meal) 
        return JsonResponse(meal_serializer.data) 
 
    elif request.method == 'PUT': 
        meal_data = JSONParser().parse(request) 
        meal_serializer = MealCreatSerializer(meal, data=meal_data) 
        if meal_serializer.is_valid(): 
            meal_serializer.save() 
            return JsonResponse(meal_serializer.data) 
        return JsonResponse(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        meal.delete() 
        return JsonResponse({'message': 'meal was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    

# get all categories,
# create new category,
# delete all categories, now in comment
@api_view(['GET', 'POST', 'DELETE'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        
        title = request.query_params.get('search', None)
        if title is not None:
            categories = categories.filter(title__icontains=title)
        
        categories_serializer = CategoryCustomSerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategoryCustomSerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
# get single category
# update category
# delete category 
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try: 
        category = Category.objects.get(pk=pk) 
    except Category.DoesNotExist: 
        return JsonResponse({'message': 'The category does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        category_serializer = CategoryCustomSerializer(category) 
        return JsonResponse(category_serializer.data) 
 
    elif request.method == 'PUT': 
        category_data = JSONParser().parse(request) 
        category_serializer = CategoryCustomSerializer(category, data=category_data) 
        if category_serializer.is_valid(): 
            category_serializer.save() 
            return JsonResponse(category_serializer.data) 
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        category.delete() 
        return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    