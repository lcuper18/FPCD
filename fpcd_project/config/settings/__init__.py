"""
Por defecto, usar configuración de desarrollo.
Para producción, establecer la variable de entorno:
export DJANGO_SETTINGS_MODULE=config.settings.production
"""

from .development import *
