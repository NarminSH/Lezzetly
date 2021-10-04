from django.urls import path
from . import views

urlpatterns = [
    path("", views.mealsApiOverviews, name="api-overview"),
    path("meals/", views.MealAPIView.as_view()),
    # path("meals/", views.meal_list),
    path("meals/<str:pk>/", views.meal_detail),
    path('categories', views.category_list),
    path('categories/<str:pk>/', views.category_detail),
    # path(r'^api/tutorials/published$', views.tutorial_list_published)
]

