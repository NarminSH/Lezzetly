
from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('frist_name', 'last_name')
    search_fields = ('frist_name', 'last_name')

