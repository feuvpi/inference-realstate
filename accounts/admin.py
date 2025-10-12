from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    # Fields to display in user list
    list_display = ['email', 'name', 'company', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_verified', 'created_at']
    search_fields = ['email', 'name', 'company', 'phone']
    ordering = ['-created_at']
    
    # Fieldsets for user detail/edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'phone')}),
        (_('Business Info'), {'fields': ('company',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for creating new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_verified'),
        }),
    )
    
    # Use email for authentication
    filter_horizontal = ('groups', 'user_permissions',)