from django.db.models import fields
from rest_framework import serializers
from ..models import Category, Ingredient, Meal, MealOption
from cooks.models import Cook


class CookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cook
        fields = (
            'first_name',
        )

class CategoryCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
            'is_taste',
            'is_time',
            'is_active',
        )

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            # 'description',
            # 'is_taste',
            # 'is_time',
            # 'status',
            # 'created_at',
            # 'updated_at',  
        )

class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = (
            'id',
            'title',
        )

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'title',
        )


class MealSerializer(serializers.ModelSerializer):
    cook = CookSerializer()
    mealoption = MealOptionSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    category = CategorySerializer(many=True)
    class Meta:
        model = Meal
        fields = (
            'id',
            'title',
            'price',
            'stock_quantity',
            'is_active',
            'created_at',
            'updated_at',
            'cook',
            'category',
            'ingredients',
            'mealoption',
        )
 
# class MealListSerializer(MealSerializer):
#     category = CategoryListSerializer(many=True)

# class MealListSerializer(MealSerializer):
#     cook = CookSerializer()