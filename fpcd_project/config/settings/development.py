"""
Configuración para entorno de desarrollo.
"""

from .base import *

DEBUG = True

# Django Debug Toolbar
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Email en consola para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
