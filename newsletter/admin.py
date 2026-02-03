from django.contrib import admin
from .models import Subscriber, NewsletterCampaign


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
    activate_subscribers.short_description = 'Activar suscriptores seleccionados'
    
    def deactivate_subscribers(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
    deactivate_subscribers.short_description = 'Desactivar suscriptores seleccionados'


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'status', 'scheduled_for', 'sent_at', 'total_recipients']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['title', 'subject']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'subject', 'devotional')
        }),
        ('Contenido', {
            'fields': ('content',)
        }),
        ('Configuración de Envío', {
            'fields': ('status', 'scheduled_for')
        }),
        ('Estadísticas', {
            'fields': ('total_recipients', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
