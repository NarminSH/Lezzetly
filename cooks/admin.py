from django.contrib import admin
from django.contrib.admin.decorators import display
from cooks.models import Cook, Resume, Recommendation
# Register your models here.

@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    list_display = ( 'first_name','last_name','created_at')
    list_filter = ( 'first_name','last_name','created_at')
    search_fields = ('first_name', 'created_at')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    display = 'created_at'


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ( 'recommended_by', 'created_at')
