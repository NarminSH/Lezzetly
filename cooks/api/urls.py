from django.urls import path
from cooks.api.views import (CookActiveOrdersAPIView, CookMealsAPIView, CookOrdersAPIView, CookRecommendationsAPIView, CooksAPIView, 
                             CookResumesAPIView, ResumesAPIView, cook_detail, cookCreate, logout, recommend_create, resume_create)

app_name = 'cooks_api'

urlpatterns = [
    path('cooks/', CooksAPIView.as_view(), name='cooks'),
    path('cooks/<int:pk>', cook_detail, name='cook'),
    path('logout/', logout, name='logout'),
    path('cook-create', cookCreate, name='cook-create'),
    path('resume-create', resume_create, name='resume-create'),
    path('recommend-create', recommend_create, name='recommend-create'),
    # path('recommendations/', RecommendationsAPIView.as_view(), name='recommendations'),
    path('resumes', ResumesAPIView.as_view(), name='resumes'),
    path('cooks/<int:pk>/recommendations', CookRecommendationsAPIView.as_view(), name='cook-recommendations'),
    path('cooks/<int:pk>/resumes', CookResumesAPIView.as_view(), name='cook-resumes'),
    path('cooks/<int:pk>/meals', CookMealsAPIView.as_view(), name='cook-meals'),
    path('cooks/<int:pk>/orders', CookOrdersAPIView.as_view(), name='cook-orders'),
    path('cooks/<int:pk>/activeorders', CookActiveOrdersAPIView.as_view(), name='cook-activeorders'),
]
