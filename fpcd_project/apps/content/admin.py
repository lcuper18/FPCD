"""
Admin configuration para la app de contenido.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Article, Devocional, EstudioBiblico, BlogPost


class CategoryAdmin(admin.ModelAdmin):
    """Admin para categorías."""

    list_display = ["name", "slug", "parent", "is_active", "created_at"]
    list_filter = ["is_active", "parent"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ["name"]}
    ordering = ["name"]


class ContentBaseAdmin(admin.ModelAdmin):
    """Admin base para contenido."""

    list_display = [
        "title",
        "author",
        "status",
        "category",
        "views",
        "published_at",
        "created_at",
    ]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["views", "created_at", "updated_at"]

    fieldsets = (
        (_("Información principal"), {"fields": ("title", "slug", "content")}),
        (_("Autor y Estado"), {"fields": ("author", "status", "category", "tags")}),
        (
            _("Imagen y SEO"),
            {
                "fields": ("featured_image", "meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Fechas y Estadísticas"),
            {
                "fields": ("published_at", "views", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Article)
class ArticleAdmin(ContentBaseAdmin):
    """Admin para artículos."""

    list_display = [
        "title",
        "author",
        "status",
        "is_featured",
        "read_time",
        "published_at",
    ]
    list_filter = ["status", "is_featured", "category"]
    list_editable = ["is_featured"]
    list_display_links = ["title"]
    search_fields = ["title", "subtitle", "content"]

    fieldsets = (
        (
            _("Información principal"),
            {"fields": ("title", "subtitle", "slug", "content")},
        ),
        (_("Autor y Estado"), {"fields": ("author", "status", "category", "tags")}),
        (_("Artículo"), {"fields": ("is_featured", "read_time")}),
        (
            _("Imagen y SEO"),
            {
                "fields": ("featured_image", "meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Fechas y Estadísticas"),
            {
                "fields": ("published_at", "views", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Devocional)
class DevocionalAdmin(ContentBaseAdmin):
    """Admin para devocionales."""

    list_display = ["title", "author", "status", "verse_reference", "date", "is_daily"]
    list_filter = ["status", "is_daily", "date"]
    list_editable = ["is_daily"]
    list_display_links = ["title"]
    search_fields = ["title", "verse_reference", "content"]
    date_hierarchy = "date"

    fieldsets = (
        (_("Información principal"), {"fields": ("title", "slug", "content")}),
        (_("Autor y Estado"), {"fields": ("author", "status", "category", "tags")}),
        (
            _("Devocional"),
            {"fields": ("verse_reference", "verse_text", "is_daily", "date")},
        ),
        (
            _("Imagen y SEO"),
            {
                "fields": ("featured_image", "meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Fechas y Estadísticas"),
            {
                "fields": ("published_at", "views", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EstudioBiblico)
class EstudioBiblicoAdmin(ContentBaseAdmin):
    """Admin para estudios bíblicos."""

    list_display = [
        "title",
        "author",
        "status",
        "bible_book",
        "bible_chapter",
        "difficulty",
    ]
    list_filter = ["status", "difficulty", "bible_book"]
    list_display_links = ["title"]
    search_fields = ["title", "bible_book", "content"]

    fieldsets = (
        (_("Información principal"), {"fields": ("title", "slug", "content")}),
        (_("Autor y Estado"), {"fields": ("author", "status", "category", "tags")}),
        (
            _("Referencia bíblica"),
            {
                "fields": (
                    "bible_book",
                    "bible_chapter",
                    "bible_verse_start",
                    "bible_verse_end",
                    "difficulty",
                    "duration",
                )
            },
        ),
        (
            _("Imagen y SEO"),
            {
                "fields": ("featured_image", "meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Fechas y Estadísticas"),
            {
                "fields": ("published_at", "views", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(BlogPost)
class BlogPostAdmin(ContentBaseAdmin):
    """Admin para entradas de blog."""

    list_display = ["title", "author", "status", "is_pinned", "views", "published_at"]
    list_filter = ["status", "is_pinned"]
    list_editable = ["is_pinned"]
    list_display_links = ["title"]
    search_fields = ["title", "excerpt", "content"]

    fieldsets = (
        (
            _("Información principal"),
            {"fields": ("title", "slug", "excerpt", "content")},
        ),
        (_("Autor y Estado"), {"fields": ("author", "status", "category", "tags")}),
        (_("Blog"), {"fields": ("is_pinned", "allow_comments")}),
        (
            _("Imagen y SEO"),
            {
                "fields": ("featured_image", "meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Fechas y Estadísticas"),
            {
                "fields": ("published_at", "views", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Category, CategoryAdmin)
