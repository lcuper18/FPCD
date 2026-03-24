"""
URL configuration for config project - FPCD
Plataforma de Enseñanza Bíblica
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # TinyMCE
    path("tinymce/", include("tinymce.urls")),
    # Portal público (raíz)
    path("", include("apps.content.urls_public")),
    # Autenticación y perfiles
    path("accounts/", include("apps.accounts.urls")),
    # Dashboard de editores/revisores
    path("dashboard/", include("apps.content.urls")),
    # Sistema de comentarios
    path("comentarios/", include("apps.comments.urls")),
    # Flujo de revisión y notificaciones
    path("workflow/", include("apps.workflow.urls")),
    # Biblioteca de medios
    path("medios/", include("apps.media_manager.urls")),
    # Newsletter y suscripciones
    path("newsletter/", include("apps.newsletter.urls")),
    # Analytics y estadísticas
    path("analytics/", include("apps.analytics.urls")),
]

# Servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
