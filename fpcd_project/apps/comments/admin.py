"""
Admin configuration para la app de comentarios.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Comment, CommentVote, CommentStatus


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin para comentarios."""

    list_display = [
        "get_author",
        "content_type",
        "get_content_preview",
        "status",
        "is_approved",
        "created_at",
    ]
    list_filter = ["status", "is_approved", "content_type", "created_at"]
    search_fields = ["content", "author__email", "author_name"]
    readonly_fields = ["created_at", "updated_at", "ip_address"]
    list_editable = ["is_approved", "status"]
    date_hierarchy = "created_at"

    fieldsets = (
        (_("Contenido"), {"fields": ("content_type", "content_id", "content")}),
        (_("Autor"), {"fields": ("author", "author_name", "author_email")}),
        (_("Respuesta"), {"fields": ("parent",)}),
        (_("Estado"), {"fields": ("status", "is_approved")}),
        (
            _("Metadata"),
            {
                "fields": ("ip_address", "user_agent", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_author(self, obj):
        return obj.get_author_name()

    get_author.short_description = _("Autor")

    def get_content_preview(self, obj):
        return obj.content[:50] + "..."

    get_content_preview.short_description = _("Contenido")


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    """Admin para votos de comentarios."""

    list_display = ["comment", "user", "vote_type", "created_at"]
    list_filter = ["vote_type", "created_at"]
    search_fields = ["comment__content", "user__email"]
    readonly_fields = ["created_at"]
