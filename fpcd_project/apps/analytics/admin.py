"""
Admin para analytics.
"""

from django.contrib import admin
from .models import PageView, DailyStats, ContentStats


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ["content_type", "object_id", "user", "ip_address", "viewed_at"]
    list_filter = ["content_type", "viewed_at"]
    search_fields = ["ip_address", "user__email"]
    ordering = ["-viewed_at"]
    readonly_fields = ["viewed_at"]

    fieldsets = (
        ("Contenido", {"fields": ("content_type", "object_id", "content_object")}),
        ("Usuario", {"fields": ("user", "session_key", "ip_address")}),
        ("Información adicional", {"fields": ("user_agent", "referrer", "viewed_at")}),
    )


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "total_views",
        "unique_visitors",
        "article_views",
        "devotional_views",
    ]
    list_filter = ["date"]
    ordering = ["-date"]
    readonly_fields = ["date"]


@admin.register(ContentStats)
class ContentStatsAdmin(admin.ModelAdmin):
    list_display = [
        "content_type",
        "object_id",
        "total_views",
        "unique_views",
        "last_viewed",
    ]
    list_filter = ["content_type"]
    ordering = ["-total_views"]
    readonly_fields = ["last_viewed"]
