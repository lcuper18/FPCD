"""
Configuración del admin para la gestión de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin personalizado para el modelo CustomUser.
    """

    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "created_at",
    ]
    list_filter = ["role", "is_active", "is_staff", "created_at"]
    search_fields = ["email", "first_name", "last_name", "username"]
    ordering = ["-created_at"]

    fieldsets = (
        (_("Información de cuenta"), {"fields": ("email", "password")}),
        (
            _("Información personal"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "bio",
                    "avatar",
                    "phone",
                )
            },
        ),
        (
            _("Permisos"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Fechas importantes"),
            {"fields": ("last_login", "created_at", "updated_at")},
        ),
    )

    add_fieldsets = (
        (_("Información de cuenta"), {"fields": ("email", "password1", "password2")}),
        (_("Información personal"), {"fields": ("first_name", "last_name", "role")}),
    )

    readonly_fields = ["created_at", "updated_at", "last_login"]

    def get_readonly_fields(self, request, obj=None):
        """Hace readonly el campo created_at."""
        return list(super().get_readonly_fields(request, obj)) + [
            "created_at",
            "updated_at",
        ]

    actions = ["make_editor", "make_reviewer", "make_admin"]

    @admin.action(description=_("Cambiar rol a Editor"))
    def make_editor(self, request, queryset):
        queryset.update(role="editor")

    @admin.action(description=_("Cambiar rol a Revisor"))
    def make_reviewer(self, request, queryset):
        queryset.update(role="reviewer")

    @admin.action(description=_("Cambiar rol a Administrador"))
    def make_admin(self, request, queryset):
        queryset.update(role="admin")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin para el modelo UserProfile.
    """

    list_display = [
        "user",
        "location",
        "website",
        "notifications_enabled",
        "created_at",
    ]
    search_fields = ["user__email", "user__first_name", "user__last_name", "location"]
    list_filter = ["notifications_enabled", "created_at"]
    raw_id_fields = ["user"]

    fieldsets = (
        (_("Usuario"), {"fields": ("user",)}),
        (
            _("Información adicional"),
            {"fields": ("location", "website", "social_links")},
        ),
        (_("Preferencias"), {"fields": ("notifications_enabled",)}),
    )
