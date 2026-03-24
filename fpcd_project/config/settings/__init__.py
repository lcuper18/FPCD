"""
Seleccionar configuración mediante la variable de entorno DJANGO_SETTINGS_MODULE.

Desarrollo:  export DJANGO_SETTINGS_MODULE=config.settings.development
Producción:  export DJANGO_SETTINGS_MODULE=config.settings.production

No importar ningún módulo aquí para evitar que los paquetes de desarrollo
(debug_toolbar, etc.) contaminen la importación de producción.
"""
