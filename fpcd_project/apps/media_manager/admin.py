"""
Admin configuration para la app de medios.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MediaFile, MediaFolder


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """Admin para archivos multimedia."""

    list_display = [
        "get_image_tag",
        "filename",
        "file_type",
        "file_size",
        "uploader",
        "created_at",
    ]
    list_filter = ["file_type", "is_active", "created_at"]
    search_fields = ["filename", "title", "description", "tags"]
    readonly_fields = ["file_size", "created_at", "updated_at", "get_image_tag"]
    list_per_page = 50

    fieldsets = (
        (_("Archivo"), {"fields": ("file", "filename", "file_type", "file_size")}),
        (_("Información"), {"fields": ("title", "description", "alt_text", "tags")}),
        (
            _("Imagen"),
            {
                "fields": ("width", "height", "thumbnail", "get_image_tag"),
                "classes": ("collapse",),
            },
        ),
        (_("Organización"), {"fields": ("folder", "used_in")}),
        (_("Estado"), {"fields": ("is_active", "uploader")}),
        (
            _("Fechas"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    """Admin para carpetas de medios."""

    list_display = ["name", "parent", "created_by", "get_file_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["created_at", "updated_at"]


# Register in existing media admin if needed
