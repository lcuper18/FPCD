from django.contrib import admin
from .models import Category, Devotional, Comment, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['user', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Devotional)
class DevotionalAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'publish_date', 'status', 'views']
    list_filter = ['status', 'category', 'publish_date', 'created_at']
    search_fields = ['title', 'content', 'bible_reference']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    inlines = [CommentInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'subtitle', 'author', 'category')
        }),
        ('Versículo Bíblico', {
            'fields': ('bible_verse', 'bible_reference')
        }),
        ('Contenido', {
            'fields': ('content', 'reflection', 'prayer')
        }),
        ('Multimedia', {
            'fields': ('featured_image',)
        }),
        ('Configuración', {
            'fields': ('status', 'publish_date', 'tags')
        }),
        ('Estadísticas', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['devotional', 'user', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'user__username']
    actions = ['approve_comments', 'disapprove_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Vista previa'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Aprobar comentarios seleccionados'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = 'Desaprobar comentarios seleccionados'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'devotional', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'devotional__title']
