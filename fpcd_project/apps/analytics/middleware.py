"""
Middleware para tracking automático de páginas vistas.
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from .services import AnalyticsService


class AnalyticsMiddleware(MiddlewareMixin):
    """
    Middleware que registra las vistas de página automáticamente.
    """

    # Rutas que no deben ser rastreadas
    EXCLUDE_PATHS = [
        "/admin/",
        "/static/",
        "/media/",
        "/favicon.ico",
        "/robots.txt",
        "/__debug__/",
    ]

    # Content types que rastreamos
    TRACKED_CONTENT_TYPES = ["article", "devocional", "estudio", "blog"]

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Verificar si debemos excluir esta ruta
        for path in self.EXCLUDE_PATHS:
            if request.path.startswith(path):
                return None

        # Solo rastrear GET requests
        if request.method != "GET":
            return None

        # Determinar el contenido basado en la URL
        content_object = self._get_content_object(request, view_kwargs)

        if content_object:
            # Usar try/except para no afectar la aplicación si falla el tracking
            try:
                AnalyticsService.track_page_view(request, content_object)
            except Exception:
                # Silenciar errores de analytics
                pass

        return None

    def _get_content_object(self, request, view_kwargs):
        """
        Determina el objeto de contenido basado en la URL.
        """
        from apps.content.models import (
            Article,
            Devocional,
            EstudioBiblico as Estudio,
            BlogPost,
        )
        from django.contrib.contenttypes.models import ContentType

        # Buscar por slug en los argumentos de la vista
        slug = view_kwargs.get("slug")

        if not slug:
            return None

        # Determinar qué modelo buscar basado en la URL
        path = request.path

        if "/articulos/" in path or "/articulo/" in path:
            try:
                return Article.objects.get(slug=slug, status="published")
            except Article.DoesNotExist:
                return None

        elif "/devocionales/" in path or "/devocional/" in path:
            try:
                return Devocional.objects.get(slug=slug, status="published")
            except Devocional.DoesNotExist:
                return None

        elif "/estudios/" in path or "/estudio/" in path:
            try:
                return Estudio.objects.get(slug=slug, status="published")
            except Estudio.DoesNotExist:
                return None

        elif "/blog/" in path:
            try:
                return BlogPost.objects.get(slug=slug, status="published")
            except BlogPost.DoesNotExist:
                return None

        return None
