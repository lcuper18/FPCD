from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administración personalizada de usuarios"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'subscribed_to_newsletter', 'is_active']
    list_filter = ['role', 'subscribed_to_newsletter', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('phone', 'bio', 'profile_picture', 'role', 'subscribed_to_newsletter')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'role')
        }),
    )
