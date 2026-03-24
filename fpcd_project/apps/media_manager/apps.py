"""
Configuración de la aplicación de gestión de medios.
"""

from django.apps import AppConfig


class MediaManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.media_manager"
    verbose_name = "Gestión de Medios"
