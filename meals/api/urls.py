from django.urls import path
from . import views

urlpatterns = [
    path("", views.mealsApiOverviews, name="api-overview"),
    path("meals/", views.mealList, name="meal-list"),
    path("meals/<str:pk>/", views.mealDetail, name="meal-detail"),
    path("meal-create/", views.mealCreate, name="meal-create"),
    path("meal-update/<str:pk>/", views.mealUpdate, name="meal-update"),
    path("meal-delete/<str:pk>/", views.mealDelete, name="meal-update"),
]
