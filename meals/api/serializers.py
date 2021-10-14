
from rest_framework import serializers
from meals.models import Category, Ingredient, Meal, MealOption
from cooks.api.serializers import CookSerializer


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

class IngredientCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
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

# when create meal
class MealCreatSerializer(serializers.ModelSerializer):
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
            # 'cook',
            'category',
            'ingredients',
            'mealoption',
        )


# when I show meals
class MealSerializer(serializers.ModelSerializer):
    cook = CookSerializer()
    mealoption = MealOptionSerializer(read_only=True, required=False, many=True)
    ingredients = IngredientSerializer(read_only=True, required=False, many=True)
    category = CategorySerializer(read_only=True, required=False, many=True)
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



# This is for orderItem
class MealOrderItemSerializer(serializers.ModelSerializer):
    # cook = CookSerializer()
    # mealoption = MealOptionSerializer(read_only=True, required=False, many=True)
    # ingredients = IngredientSerializer(read_only=True, required=False, many=True)
    # category = CategorySerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Meal
        fields = (
            'id',
            'title',
            'price',
            'stock_quantity',
            'is_active',
        )


# class MealListSerializer(MealSerializer):
#     category = CategoryListSerializer(many=True)

# class MealListSerializer(MealSerializer):
#     cook = CookSerializer()