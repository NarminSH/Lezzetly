from django.urls import path
from . import views

# all meals apis is alraady done 

urlpatterns = [
    path("", views.mealsApiOverviews, name="api-overview"),
    path("meals/", views.MealAPIView.as_view()),
    # path("meals/<str:pk>/", views.meal_single),
    path("meal-create/", views.meal_list),
    path("meals/<str:pk>/", views.meal_detail),
    path('categories/', views.category_list),
    path('categories/<str:pk>/', views.category_detail),
    path('mealoptions/', views.mealoption_list),
    path('mealoptions/<str:pk>/', views.mealoption_detail),
    path('ingredients/', views.ingredient_list),
    path('ingredients/<str:pk>/', views.ingredient_detail),
    # path(r'^api/tutorials/published$', views.tutorial_list_published)
]

