from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'profile_picture', 'following')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'following')
