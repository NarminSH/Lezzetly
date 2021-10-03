from django.urls import path
from . import views

urlpatterns = [
    path("", views.mealsApiOverviews, name="api-overview"),
    path("meals/", views.MealAPIView.as_view(), name="meal-list"),
    path("meals/<str:pk>/", views.mealDetail, name="meal-detail"),
    path("meal-create/", views.mealCreate, name="meal-create"),
    path("meal-update/<str:pk>/", views.mealUpdate, name="meal-update"),
    path("meal-delete/<str:pk>/", views.mealDelete, name="meal-update"),
    # path("categories/", views.CategoryList.as_view(), name="category-list"),
    # path("categories/<str:pk>/", views.CategoryDetailAPIView.as_view(), name="category-detail"),
    # path("categories/", views.CategoryDetailAPIView.as_view(), name="category-create"),
    # path("categories/<str:pk>/", views.UpdateCategoryAPIView.as_view(), name="category-update"),
    # path(r'^categories$', views.category_list),
    path('categories', views.category_list),
    path('categories/<str:pk>/', views.category_detail),
    # path(r'^api/tutorials/published$', views.tutorial_list_published)
]

# urlpatterns = [ 
#     url(r'^api/tutorials$', views.tutorial_list),
#     url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
#     url(r'^api/tutorials/published$', views.tutorial_list_published)
# ]
