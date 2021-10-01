from django.urls import path

from cooks.api.views import RecommendationAPIView, CooksAPIView, CookAPIView, RecommendationsAPIView, ResumesAPIView, ResumeAPIView

app_name = 'cooks_api'

urlpatterns = [
    path('cooks/', CooksAPIView.as_view(), name='cooks'),
    path('cooks/<int:pk>', CookAPIView.as_view(), name='cook'),
    path('recommendations/', RecommendationsAPIView.as_view(), name='recommendations'),
    path('resumes/', ResumesAPIView.as_view(), name='resumes'),
    path('cooks/<int:pk>/recommendations/', RecommendationAPIView.as_view(), name='cook-recommendations'),
    path('cooks/<int:pk>/resumes/', ResumeAPIView.as_view(), name='cook-resumes'),
    # path('cooks/<int:pk>/meals/', RecommendationAPIView.as_view(), name='user-meals'),

]
