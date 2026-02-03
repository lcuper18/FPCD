from django.conf import settings


def site_context(request):
    """Context processor para agregar información del sitio a todas las plantillas"""
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'Fe para Cada Día'),
        'youtube_url': getattr(settings, 'YOUTUBE_CHANNEL_URL', ''),
    }
