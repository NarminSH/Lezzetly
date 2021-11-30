from django.urls import path
from . import views

# all meals apis is alraady done 

urlpatterns = [
    path("", views.mealsApiOverviews, name="api-overview"),
    path("meals", views.MealAPIView.as_view()),
    # path("meals/<str:pk>/", views.meal_single),
    path("meal-create/", views.meal_create),
    # path("meal-create/", views.UploadFileAndJson.as_view()),
    path("meals/<str:pk>", views.meal_detail),
    path("meal/<str:pk>", views.meal_single),
    path('categories', views.CategoryAPIView.as_view()),
    path('category-create', views.category_list),
    path('categories/<str:pk>', views.category_detail),
    path('mealoptions', views.MealOptionAPIView.as_view()),
    path('mealoption-create', views.mealoption_list),
    path('mealoptions/<str:pk>', views.mealoption_detail),
    path('ingredients', views.IngredientOptionAPIView.as_view()),
    path('ingredient-create', views.ingredient_list),
    path('ingredients/<str:pk>', views.ingredient_detail),
    # path(r'^api/tutorials/published$', views.tutorial_list_published)
]

