import django_filters
from ..models import Meal


class MealFilter(django_filters.FilterSet):
    class Meta:
        model = Meal
        fields = ['title', 'price', 'category__title', 'ingredients__title', 'mealoption__title']