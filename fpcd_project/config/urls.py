"""
URL configuration for config project - FPCD
Plataforma de Enseñanza Bíblica
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.content.views_public import HomeView
from .views_health import health_check

urlpatterns = [
    # Health check endpoint for load balancers
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("content/", include("apps.content.urls", namespace="content")),
    path("content/", include("apps.content.urls_public", namespace="public")),
    path("workflow/", include("apps.workflow.urls", namespace="workflow")),
    path("media/", include("apps.media_manager.urls", namespace="media_manager")),
    # Root URL - provides 'home' for reverse()
    path("", HomeView.as_view(), name="home"),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
