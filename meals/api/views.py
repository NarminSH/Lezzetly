from re import search
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import filters
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CategoryCustomSerializer, MealSerializer, CategoryUpdateSerializer
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
        'Update meal': '/meal-update/<str:pk>',
        'Delete meal': '/meal-delete/<str:pk>',
        # 'List of categories': '/categories'
    }
    return Response(api_urls)

# Api for  get all meals and for search
# for search - meals/?search=lunch 
class MealAPIView(generics.ListCreateAPIView):
    search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title']
    filter_backends = (filters.SearchFilter,)
    queryset = Meal.objects.filter(is_active=True)
    serializer_class = MealSerializer

# get one meal
@api_view(['GET'])
def mealDetail(request, pk):
    meal = Meal.objects.get(id=pk)
    serializer = MealSerializer(meal, many=False)
    return Response(serializer.data)

# create new meal
@api_view(['POST'])
def mealCreate(request):
    serializer = MealSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# update meal
@api_view(['PUT'])
def mealUpdate(request, pk):
    meal = Meal.objects.get(id=pk)
    serializer = MealSerializer(instance=meal, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# delete meal
@api_view(['DELETE'])
def mealDelete(request, pk):
    meal = Meal.objects.get(id=pk)
    meal.delete()
    return Response("Successfully deleted!")

# get all categories
# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.filter(is_active = True)
#     serializer_class = CategoryCustomSerializer

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = CategoryCustomSerializer(queryset, many=True)
#         return Response(serializer.data)

# get all categories
# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.filter(is_active = True)
#     serializer_class = CategoryCustomSerializer

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = CategoryCustomSerializer(queryset, many=True)
#         return Response(serializer.data)

# get one category
# class CategoryDetailAPIView(APIView):
#     def get(self,request,pk):
#         category = Category.objects.get(id=pk)
#         serializer = CategoryCustomSerializer(category, many=False)
#         return Response(serializer.data)

# create category
# class CreateCategoryAPIView(APIView):
#     def post(self,request):
#         serializer = CategoryCustomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

# update category
# class UpdateCategoryAPIView(APIView):
#     def post(self,request,pk):
#         category = Category.objects.get(id=pk)
#         serializer = CategoryUpdateSerializer(instance=category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

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
    
    elif request.method == 'DELETE':
        count = Category.objects.all().delete()
        return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
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
    