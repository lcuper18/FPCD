from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'category', 'is_published', 'is_featured', 'views', 'downloads']
    list_filter = ['material_type', 'is_published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'description', 'material_type', 'category')
        }),
        ('Contenido', {
            'fields': ('content', 'file', 'external_url', 'thumbnail')
        }),
        ('Configuración', {
            'fields': ('author', 'tags', 'is_published', 'is_featured')
        }),
        ('Estadísticas', {
            'fields': ('views', 'downloads'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
