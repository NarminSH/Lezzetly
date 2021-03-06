import re
from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import permissions
from rest_framework.settings import reload_api_settings
from rest_framework.utils import json
from cooks.models import Cook
from users.api.jwt import JWTAuthentication
from django.contrib.auth.models import Permission
from users.models import User
from utility.check_token import checkToken
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
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from drf_yasg import openapi
# import sys
# reload_api_settings(sys)
# sys.setdefaultencoding("utf-8")
 
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
    queryset = Meal.objects.filter(is_active=True)
    serializer_class = MealSerializer


test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@swagger_auto_schema(method = 'POST',request_body=MealCreatSerializer)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser])
def meal_create(request):
    # print("***************")
    # print("Entered to meal create")
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'warning': 'Only cook can create meal!'}, status=status.HTTP_200_OK)
    else:
        try:
            currentCook = Cook.objects.get(username = claimsOrMessage['Username'])
        except Cook.DoesNotExist: 
            return JsonResponse({'warning': 'Invalid token, this cook not exists!'}, status=status.HTTP_200_OK)
        print("meal_create current cook: ", currentCook)
        # custom_queryset = request.user.filter(is_available=True, service_place__isnull=False, 
        #                         rating__isnull=False, payment_address__isnull=False, work_experience__isnull=False)
        # datam = JSONParser().parse(request.data)
        print("//////////")
        print("meal create-da Data category", request.data)
        # print("meal create-da Data category", request.data['category'])
        print("//////////")
        is_full = False
        if currentCook.is_available is not None and currentCook.service_place is not None and currentCook.payment_address is not None and currentCook.work_experience is not None:
            is_full = True
        queryset = Cook.objects.filter(is_available=True, service_place__isnull=False, 
                                rating__isnull=False, payment_address__isnull=False, work_experience__isnull=False)
        # meal_data = JSONParser().parse(request)
        print("************")
        # print("meal_data: ", meal_data)
        print("************")
        # print("+++++get_user: ", request.user)
        # print("++++++++ get is_full:", is_full)
        # print("+++++get_queryset: ", queryset)
        if request.method == 'POST' and claimsOrMessage['Usertype'] != "1":
            return JsonResponse({'warning': 'Only Cook may create meal!'}, status=status.HTTP_200_OK)
        if request.method == 'POST' and not is_full:
            return JsonResponse({'warning': 'Please fill in required information in your profile!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('category') and not request.data.get('ingredients') and not request.data.get('mealoption'):
            return JsonResponse({'warning': 'You have to add category, mealoption and ingredients!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('category') and not request.data.get('ingredients'):
            return JsonResponse({'warning': 'You have to add category and ingredients!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('category') and not request.data.get('mealoption'):
            return JsonResponse({'warning': 'You have to add category and mealoption!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('category'):
            return JsonResponse({'warning': 'You have to add category!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('ingredients') and not request.data.get('mealoption'):
            return JsonResponse({'warning': 'You have to add ingredients and mealoption!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('mealoption'):
            return JsonResponse({'warning': 'You have to add mealoption!'}, status=status.HTTP_200_OK)
        elif request.method == 'POST' and not request.data.get('ingredients'):
            return JsonResponse({'ingredient': 'You have to add ingredients!'}, status=status.HTTP_200_OK)
        print("Category printine kimi geldi")
        # print("meap data", meal_data['category'])
        # print(request.user)
        # , safe=False
        meal_serializer = MealCreatSerializer(data=request.data)
        # print(meal_data, 'asdfghjkl')
        # print(meal_data['cook'], 'qwsdfgasdfghdefrgher')
        if meal_serializer.is_valid():
            # print("mealCreate ", isinstance(request.user, User))
            meal_serializer.save(cook = currentCook)
            # print(meal_serializer, 'jshckjdsbcfhjdx')
            return JsonResponse(meal_serializer.data, safe=False, status=status.HTTP_201_CREATED)
        else:
            print(meal_serializer.errors)
            return JsonResponse(meal_serializer.errors, status=status.HTTP_200_OK) 
        # return JsonResponse(meal_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        



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
# @swagger_auto_schema(method = 'GET',request_body=MealSerializer)

test_param_meal = openapi.Parameter('test', openapi.IN_QUERY, description="id in parametr is important", type=openapi.TYPE_BOOLEAN)
user_response_meal = openapi.Response('Asagidaki Melumatlar qayidir', MealSerializer)

@swagger_auto_schema(method='get', manual_parameters=[test_param_meal], responses={200: user_response_meal})
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def meal_single(request, pk):
    # token = request.GET.get('token')
    # print("request.token", request.token)
    try: 
        meal = Meal.objects.get(pk=pk, is_active=True)
        print("meal inside singe meal: ", meal) 
    except Meal.DoesNotExist: 
        return JsonResponse({'message': 'The meal does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        meal_serializer = MealSerializer(meal) 
        return JsonResponse(meal_serializer.data) 
 



# update meal
# delete meal

test_param_delete = openapi.Parameter('delete', openapi.IN_QUERY, description="id in parametr is important", type=openapi.TYPE_BOOLEAN)
# user_response_meal = openapi.Response('Asagidaki Melumatlar qayidir', MealSerializer)

@swagger_auto_schema(methods=['delete'], manual_parameters=[test_param_meal], responses={200: "meal was deleted successfully"})
@swagger_auto_schema(methods=['patch'], request_body=MealCreatSerializer)
@api_view(['PATCH', 'DELETE'])
# @authentication_classes([])
# @permission_classes([IsAuthenticated,])
@authentication_classes([])
@permission_classes([])
def meal_detail(request, pk):
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'warning': 'Only cook can update or delete meal!'}, status=status.HTTP_200_OK)
    
    # token = request.GET.get('token')
    # print("request.token", request.token)
    try: 
        meal = Meal.objects.get(pk=pk) 
    except Meal.DoesNotExist: 
        return JsonResponse({'message': 'The meal does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    cookUserName = meal.cook.username
    userInToken = claimsOrMessage['Username']
    # print("***** inside meal_detail ********")
    # print("cookId", cookId)
    # print("userInRequestId", userInRequestId)
    # print("***** inside meal_detail ********")
    # if request.method == 'GET':
    #     meal_serializer = MealSerializer(meal) 
    #     return JsonResponse(meal_serializer.data) 
 
    # if request.method == 'PATCH' and isinstance(request.user, Cook) == False:
    #     return JsonResponse({'message': 'Only cook can update meal!'}, status=status.HTTP_200_OK)
    if request.method == 'PATCH' and claimsOrMessage['Usertype'] == "1" and cookUserName != userInToken:
        return JsonResponse({'message': 'You have not permission update this meal!'}, status=status.HTTP_200_OK)
    elif request.method == 'PATCH' and claimsOrMessage['Usertype'] == "1" and cookUserName == userInToken:
        # print("jwt decode: ", payload = JWTAuthentication.decode(token, settings.SECRET_KEY, algorithms="HS256"))
        # return JsonResponse({'message': 'terminala bax!'}, status=status.HTTP_200_OK)
    # elif request.method == 'PATCH':
    #     print("Token", token)
    #     data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    #     print("jwt decode: ", data)
    #     return JsonResponse({'message': 'terminala bax!'}, status=status.HTTP_200_OK)

    # # if request.method == 'PATCH': 
        meal_data = JSONParser().parse(request)
        orderItemsOfMeal = meal.ordered_items.all()
        # print("+++++ orderItemsOfMeal: ", orderItemsOfMeal)
        is_in_active_order = False
        for i in orderItemsOfMeal:
            if i.order.complete == False:
                is_in_active_order = True
            # print("OrderItemWithMeal.complete: ", i.order.complete)
        if is_in_active_order:
            return JsonResponse({'message': 'This meal in active order you can not change it!'}, status=status.HTTP_200_OK)
        else:
            meal_serializer = MealCreatSerializer(meal, data=meal_data, partial=True) 
            if meal_serializer.is_valid(): 
                meal_serializer.save() 
                return JsonResponse(meal_serializer.data) 
        return JsonResponse(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    # elif request.method == 'DELETE' and isinstance(request.user, Cook) == False:
    #     return JsonResponse({'message': 'Only cook can update meal!'}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE' and claimsOrMessage['Usertype'] == "1" and cookUserName != userInToken:
        return JsonResponse({'message': 'You have not permission delete this meal!'}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE' and claimsOrMessage['Usertype'] == "1" and cookUserName == userInToken:
        queryset = meal.ordered_items.all()
        if not queryset:
            meal.delete()
            return JsonResponse({'message': 'meal was deleted successfully!'}, status=status.HTTP_200_OK)
        else:
            check_count = 0
            for i in queryset:
                if i.order.complete == False:
                    check_count += 1
            if check_count != 0:
                return JsonResponse({'message': 'You can not delete this meal, this meal in active order!'}, status=status.HTTP_200_OK)    
            else:
                # print("************")
                # print("mealin statusu delete-den evvel: ", meal.is_active)
                meal.is_active = False
                meal.save()
                # print("mealin statusu delete-den sonra: ", meal.is_active)
                # print("************")
                return JsonResponse({'message': 'meal status changed to not active successfully!'}, status=status.HTTP_200_OK)


# get all categories,
class CategoryAPIView(generics.ListAPIView):
    # authentication_classes = []
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryCustomSerializer


# create new category,
# delete all categories, now in comment
test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', MealCreatSerializer)

# 'method' can be used to customize a single HTTP method of a view
# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(method = 'POST',request_body=CategoryCustomSerializer)
@api_view(['POST'])
# @authentication_classes([])
# @permission_classes([IsAuthenticated,])
@authentication_classes([])
@permission_classes([])
def category_list(request):
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK) 
    
    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'message': 'Only cook can get, create and update category!'}, status=status.HTTP_200_OK)
    else:
        # if request.method == 'GET':
        #     categories = Category.objects.all()
            
        #     title = request.query_params.get('search', None)
        #     if title is not None:
        #         categories = categories.filter(title__icontains=title)
            
        #     categories_serializer = CategoryCustomSerializer(categories, many=True)
        #     return JsonResponse(categories_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        if request.method == 'POST':
            category_data = JSONParser().parse(request)
            category_serializer = CategoryCustomSerializer(data=category_data)
            if category_serializer.is_valid(raise_exception=True):
                category_serializer.save()
                return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED) 
            # return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(category_serializer.errors)
                return JsonResponse(category_serializer.errors, status=status.HTTP_200_OK)
        
    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
# get single category
# update category
# delete category
test_param_category = openapi.Parameter('category', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
user_response_category = openapi.Response('Asagidaki Melumatlar qayidir', CategoryCustomSerializer)


@swagger_auto_schema(methods=['get', 'put'], manual_parameters=[test_param_category], responses={200: user_response_category}) 
@swagger_auto_schema(methods=['delete'], manual_parameters=[test_param_category], responses={200: "category was deleted successfully"})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try: 
        category = Category.objects.get(pk=pk) 
    except Category.DoesNotExist: 
        return JsonResponse({'message': 'The category does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if isinstance(request.user, Cook) == False:
        return JsonResponse({'message': 'Only cook can get, create and update category!'}, status=status.HTTP_200_OK)
    else:
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
            return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_200_OK)

# get all mealoptions,
class MealOptionAPIView(generics.ListAPIView):
    # authentication_classes = []
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = MealOption.objects.filter(is_active=True)
    serializer_class = MealOptionSerializer

# mealoption

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', MealCreatSerializer)

# 'method' can be used to customize a single HTTP method of a view
# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(method = 'POST',request_body=MealOptionSerializer)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
# @permission_classes([IsAuthenticated])
def mealoption_list(request):
    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
    if claimsOrMessage['Usertype'] != "1": 
        return JsonResponse({'message': 'Only cook can get, create and update mealoption!'}, status=status.HTTP_200_OK)
    else:
        # if request.method == 'GET':
        #     mealoptions = MealOption.objects.all()
            
        #     title = request.query_params.get('search', None)
        #     if title is not None:
        #         mealoptions = mealoptions.filter(title__icontains=title)
            
        #     mealoptions_serializer = MealOptionSerializer(mealoptions, many=True)
        #     return JsonResponse(mealoptions_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        if request.method == 'POST':
            mealoption_data = JSONParser().parse(request)
            mealoption_serializer = MealOptionSerializer(data=mealoption_data)
            if mealoption_serializer.is_valid(raise_exception=True):
                mealoption_serializer.save()
                return JsonResponse(mealoption_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(mealoption_serializer.errors, status=status.HTTP_200_OK)

# get single mealoption
# update mealoption
# delete mealoption
test_param_mealoption = openapi.Parameter('mealoption', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
user_response_mealoption = openapi.Response('Asagidaki Melumatlar qayidir', MealOptionSerializer)

@swagger_auto_schema(methods=['get', 'put'], manual_parameters=[test_param_mealoption], responses={200: user_response_mealoption}) 
@swagger_auto_schema(methods=['delete'], manual_parameters=[test_param_mealoption], responses={200: "mealoption was deleted successfully"})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def mealoption_detail(request, pk):
    try: 
        mealoption = MealOption.objects.get(pk=pk) 
    except MealOption.DoesNotExist: 
        return JsonResponse({'message': 'The meal option does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if isinstance(request.user, Cook) == False:
        return JsonResponse({'message': 'Only cook can get, create and update mealoption!'}, status=status.HTTP_200_OK)
    else:
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
            return JsonResponse({'message': 'Meal option was deleted successfully!'}, status=status.HTTP_200_OK)

# get all ingredients,
class IngredientOptionAPIView(generics.ListAPIView):
    # authentication_classes = []
    authentication_classes = []
    permission_classes = []
    # search_fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title', 'cook__first_name']
    # filter_backends = (filters.SearchFilter,)
    queryset = Ingredient.objects.filter(is_active=True)
    serializer_class = IngredientCustomSerializer


# get all ingredients,
# create new ingredient,
# delete all ingredients, now in comment
test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', MealCreatSerializer)

# 'method' can be used to customize a single HTTP method of a view
# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(method = 'POST',request_body=IngredientCustomSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@authentication_classes([])
@permission_classes([])
def ingredient_list(request):

    tokenStr = request.META.get('HTTP_AUTHORIZATION')
    claimsOrMessage = checkToken(tokenStr)
    if 'warning' in claimsOrMessage:
        return JsonResponse(claimsOrMessage, status=status.HTTP_200_OK)
    
    if claimsOrMessage['Usertype'] != "1":
        return JsonResponse({'message': 'Only cook can get, create and update ingredients!'}, status=status.HTTP_200_OK)
    else:
        # if request.method == 'GET':
        #     ingredients = Ingredient.objects.all()
            
        #     title = request.query_params.get('search', None)
        #     if title is not None:
        #         ingredients = ingredients.filter(title__icontains=title)
            
        #     ingredient_serializer = IngredientCustomSerializer(ingredients, many=True)
        #     return JsonResponse(ingredient_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        if request.method == 'POST':
            ingredient_data = JSONParser().parse(request)
            ingredient_serializer = IngredientCustomSerializer(data=ingredient_data)
            if ingredient_serializer.is_valid(raise_exception=True):
                ingredient_serializer.save()
                return JsonResponse(ingredient_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # elif request.method == 'DELETE':
    #     count = Category.objects.all().delete()
    #     return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
# get single ingredient
# update ingredient
# delete ingredient
test_param_ingredient = openapi.Parameter('ingredient', openapi.IN_QUERY, description="id in parametr is important and login as cook", type=openapi.TYPE_BOOLEAN)
user_response_ingredient = openapi.Response('Asagidaki Melumatlar qayidir', IngredientCustomSerializer)

@swagger_auto_schema(methods=['get', 'put'], manual_parameters=[test_param_ingredient], responses={200: user_response_ingredient}) 
@swagger_auto_schema(methods=['delete'], manual_parameters=[test_param_ingredient], responses={200: "ingredient was deleted successfully"})
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def ingredient_detail(request, pk):
    try: 
        ingredient = Ingredient.objects.get(pk=pk) 
    except Ingredient.DoesNotExist: 
        return JsonResponse({'message': 'The ingredient does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if isinstance(request.user, Cook) == False:
        return JsonResponse({'message': 'Only cook can get, create and update ingredients!'}, status=status.HTTP_200_OK)
    else:
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
            return JsonResponse({'message': 'Ingredient was deleted successfully!'}, status=status.HTTP_200_OK)

