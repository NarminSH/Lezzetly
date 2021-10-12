from django.db.models.query import QuerySet
from rest_framework import permissions
from cooks.models import Cook
from users.models import User
from .filters import MealFilter
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CategoryCustomSerializer, MealOptionSerializer, MealSerializer, MealCreatSerializer, CategoryUpdateSerializer, IngredientCustomSerializer
from ..models import Category, Ingredient, Meal, MealOption
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
    permission_classes = []
    search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
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
@permission_classes([IsAuthenticated])
def meal_list(request):
    # custom_queryset = request.user.filter(is_available=True, service_place__isnull=False, 
    #                         rating__isnull=False, payment_address__isnull=False, work_experience__isnull=False)
    is_full = False
    if request.user.is_available is not None and request.user.service_place is not None and request.user.payment_address is not None and request.user.work_experience is not None:
        is_full = True
    queryset = Cook.objects.filter(is_available=True, service_place__isnull=False, 
                            rating__isnull=False, payment_address__isnull=False, work_experience__isnull=False)
    # print("+++++get_user: ", request.user)
    # print("++++++++ get is_full:", is_full)
    # print("+++++get_queryset: ", queryset)
    if request.method == 'POST' and not isinstance(request.user, Cook):
        return JsonResponse({'message': 'Only Cook may create meal!'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'POST' and not is_full:
        return JsonResponse({'message': 'Please fill in required information in your profile!'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'POST':    
        print(request.user)
        meal_data = JSONParser().parse(request)
        meal_serializer = MealCreatSerializer(data=meal_data)
        print(meal_data, 'asdfghjkl')
        # print(meal_data['cook'], 'qwsdfgasdfghdefrgher')
        if meal_serializer.is_valid():
            # print("mealCreate ", isinstance(request.user, User))
            meal_serializer.save(cook = request.user)
            # print(meal_serializer, 'jshckjdsbcfhjdx')
            return JsonResponse(meal_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([AllowAny])
# def meal_single(request, pk):
#     try: 
#         meal = Meal.objects.get(pk=pk) 
#     except Meal.DoesNotExist: 
#         return JsonResponse({'message': 'The meal does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
#     if request.method == 'GET': 
#         meal_serializer = MealSerializer(meal) 
#         return JsonResponse(meal_serializer.data) 

# get single meal
# update meal
# delete meal 
@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def meal_detail(request, pk):
    try: 
        meal = Meal.objects.get(pk=pk) 
    except Meal.DoesNotExist: 
        return JsonResponse({'message': 'The meal does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        meal_serializer = MealSerializer(meal) 
        return JsonResponse(meal_serializer.data) 
 
    elif request.method == 'PATCH': 
    # if request.method == 'PATCH': 
        meal_data = JSONParser().parse(request)
        print("+++++ meal data: ", meal_data) 
        meal_serializer = MealCreatSerializer(meal, data=meal_data) 
        if meal_serializer.is_valid(): 
            meal_serializer.save() 
            return JsonResponse(meal_serializer.data) 
        return JsonResponse(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE':
        queryset = meal.ordered_items.all()
        if not queryset:
            meal.delete()
            return JsonResponse({'message': 'meal was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            check_count = 0
            for i in queryset:
                if i.order.complete == False:
                    check_count += 1
            if check_count != 0:
                return JsonResponse({'message': 'You can not delete this meal, this meal in active order!'}, status=status.HTTP_403_FORBIDDEN)    
            else:
                meal.is_active = False
                return JsonResponse({'message': 'meal status changed to not active successfully!'}, status=status.HTTP_204_NO_CONTENT)

# get all categories,
# create new category,
# delete all categories, now in comment
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
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
@authentication_classes([])
@permission_classes([AllowAny])
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

    
# mealoption
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def mealoption_list(request):
    if request.method == 'GET':
        mealoptions = MealOption.objects.all()
        
        title = request.query_params.get('search', None)
        if title is not None:
            mealoptions = mealoptions.filter(title__icontains=title)
        
        mealoptions_serializer = MealOptionSerializer(mealoptions, many=True)
        return JsonResponse(mealoptions_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        mealoption_data = JSONParser().parse(request)
        mealoption_serializer = MealOptionSerializer(data=mealoption_data)
        if mealoption_serializer.is_valid():
            mealoption_serializer.save()
            return JsonResponse(mealoption_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(mealoption_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get single mealoption
# update meal
# delete meal 
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def mealoption_detail(request, pk):
    try: 
        mealoption = MealOption.objects.get(pk=pk) 
    except MealOption.DoesNotExist: 
        return JsonResponse({'message': 'The meal option does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        mealoption_serializer = MealOptionSerializer(mealoption) 
        return JsonResponse(mealoption_serializer.data)
 
    elif request.method == 'PUT': 
        mealoption_data = JSONParser().parse(request) 
        mealoption_serializer = MealOptionSerializer(mealoption, data=mealoption_data) 
        if mealoption_serializer.is_valid(): 
            mealoption_serializer.save() 
            return JsonResponse(mealoption_serializer.data) 
        return JsonResponse(mealoption_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        mealoption.delete() 
        return JsonResponse({'message': 'Meal option was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    

# get all ingredients,
# create new ingredient,
# delete all ingredients, now in comment
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def ingredient_list(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        
        title = request.query_params.get('search', None)
        if title is not None:
            ingredients = ingredients.filter(title__icontains=title)
        
        ingredient_serializer = IngredientCustomSerializer(ingredients, many=True)
        return JsonResponse(ingredient_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        ingredient_data = JSONParser().parse(request)
        ingredient_serializer = IngredientCustomSerializer(data=ingredient_data)
        if ingredient_serializer.is_valid():
            ingredient_serializer.save()
            return JsonResponse(ingredient_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
# get single ingredient
# update ingredient
# delete ingredient
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def ingredient_detail(request, pk):
    try: 
        ingredient = Ingredient.objects.get(pk=pk) 
    except Ingredient.DoesNotExist: 
        return JsonResponse({'message': 'The ingredient does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        ingredient_serializer = IngredientCustomSerializer(ingredient) 
        return JsonResponse(ingredient_serializer.data) 
 
    elif request.method == 'PUT': 
        ingredient_data = JSONParser().parse(request) 
        ingredient_serializer = IngredientCustomSerializer(ingredient, data=ingredient_data) 
        if ingredient_serializer.is_valid(): 
            ingredient_serializer.save() 
            return JsonResponse(ingredient_serializer.data) 
        return JsonResponse(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        ingredient.delete() 
        return JsonResponse({'message': 'Ingredient was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

