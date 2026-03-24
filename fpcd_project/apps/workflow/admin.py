"""
Admin configuration para la app de workflow.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Review, Notification, ContentSubmission


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin para revisiones."""

    list_display = ["__str__", "reviewer", "author", "status", "created_at"]
    list_filter = ["status", "content_type", "created_at"]
    search_fields = ["content_type", "content_id", "comment", "feedback"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (_("Contenido"), {"fields": ("content_type", "content_id")}),
        (_("Participantes"), {"fields": ("reviewer", "author")}),
        (_("Revisión"), {"fields": ("status", "comment", "feedback")}),
        (
            _("Fechas"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin para notificaciones."""

    list_display = ["user", "notification_type", "title", "is_read", "created_at"]
    list_filter = ["is_read", "notification_type", "created_at"]
    search_fields = ["title", "message", "user__email"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (_("Usuario"), {"fields": ("user",)}),
        (
            _("Notificación"),
            {"fields": ("notification_type", "title", "message", "link")},
        ),
        (_("Estado"), {"fields": ("is_read", "read_at")}),
        (_("Fecha"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(ContentSubmission)
class ContentSubmissionAdmin(admin.ModelAdmin):
    """Admin para envíos de contenido."""

    list_display = ["__str__", "author", "submitted_at", "reviewed_at"]
    list_filter = ["content_type", "submitted_at"]
    search_fields = ["content_type", "content_id", "author__email"]
    readonly_fields = ["submitted_at"]
    date_hierarchy = "submitted_at"
