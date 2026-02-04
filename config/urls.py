"""
URL configuration for Fe para Cada Día project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.devotionals.urls')),
    path('usuarios/', include('src.users.urls')),
    path('newsletter/', include('src.newsletter.urls')),
    path('materiales/', include('src.materials.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Customize admin site
admin.site.site_header = "Fe para Cada Día - Administración"
admin.site.site_title = "Fe para Cada Día Admin"
admin.site.index_title = "Panel de Administración"

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
