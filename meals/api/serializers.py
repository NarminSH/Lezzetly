
from rest_framework import serializers
from meals.models import Category, Ingredient, Meal, MealOption
from cooks.api.serializers import CookPublicSerializer, CookSerializer


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
            'image',
            'stock_quantity',
            'is_active',
            'category',
            'ingredients',
            'mealoption',
            'preparing_time',
            'created_at',
            'updated_at',
            # 'cook',
        )



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


# when I show meals
class MealSerializer(DynamicFieldsModelSerializer):
    cook = CookPublicSerializer()
    mealoption = MealOptionSerializer(read_only=True, required=False, many=True)
    ingredients = IngredientSerializer(read_only=True, required=False, many=True)
    category = CategorySerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Meal
        fields = (
            'id',
            'title',
            'price',
            'image',
            'stock_quantity',
            'quantity',
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