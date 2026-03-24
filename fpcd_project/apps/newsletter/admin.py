"""
Admin para newsletter y suscripciones.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Subscriber, Newsletter, NewsletterArchive


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Admin para suscriptores.
    """

    list_display = ["email", "first_name", "is_active", "is_verified", "subscribed_at"]
    list_filter = ["is_active", "is_verified", "subscribed_at"]
    search_fields = ["email", "first_name"]
    ordering = ["-subscribed_at"]
    readonly_fields = ["subscribed_at", "unsubscribed_at", "verification_token"]

    fieldsets = (
        (_("Información"), {"fields": ("email", "first_name")}),
        (_("Estado"), {"fields": ("is_active", "is_verified", "verification_token")}),
        (
            _("Fechas"),
            {"fields": ("subscribed_at", "unsubscribed_at", "unsubscribed_reason")},
        ),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin para boletines.
    """

    list_display = ["subject", "status", "sent_at", "recipient_count", "created_by"]
    list_filter = ["status", "created_at", "sent_at"]
    search_fields = ["subject", "content"]
    ordering = ["-created_at"]
    readonly_fields = [
        "sent_at",
        "recipient_count",
        "open_count",
        "click_count",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (_("Contenido"), {"fields": ("subject", "content", "content_html")}),
        (_("Estado"), {"fields": ("status", "sent_at", "scheduled_for")}),
        (
            _("Estadísticas"),
            {"fields": ("recipient_count", "open_count", "click_count")},
        ),
        (_("Información"), {"fields": ("created_by", "created_at", "updated_at")}),
    )


@admin.register(NewsletterArchive)
class NewsletterArchiveAdmin(admin.ModelAdmin):
    """
    Admin para archivos de boletines.
    """

    list_display = ["subject", "sent_at", "recipient_count", "open_count"]
    search_fields = ["subject", "content_html"]
    ordering = ["-sent_at"]
    readonly_fields = [
        "sent_at",
        "subject",
        "content_html",
        "recipient_count",
        "open_count",
    ]
