from django.urls import path
from cooks.api.views import (CookMealsAPIView, CookRecommendationsAPIView, CooksAPIView, 
                            CookAPIView, RecommendationsAPIView, ResumesAPIView, CookResumesAPIView)

app_name = 'cooks_api'

urlpatterns = [
    path('cooks/', CooksAPIView.as_view(), name='cooks'),
    path('cooks/<int:pk>', CookAPIView.as_view(), name='cook'),
    path('recommendations/', RecommendationsAPIView.as_view(), name='recommendations'),
    path('resumes/', ResumesAPIView.as_view(), name='resumes'),
    path('cooks/<int:pk>/recommendations/', CookRecommendationsAPIView.as_view(), name='cook-recommendations'),
    path('cooks/<int:pk>/resumes/', CookResumesAPIView.as_view(), name='cook-resumes'),
    path('cooks/<int:pk>/meals/', CookMealsAPIView.as_view(), name='cook-meals'),

]
