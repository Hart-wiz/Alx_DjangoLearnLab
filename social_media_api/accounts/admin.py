from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'followers')
