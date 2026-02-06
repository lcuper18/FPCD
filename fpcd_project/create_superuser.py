#!/usr/bin/env python
"""
Script para crear el superusuario inicial del proyecto FPCD
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@fpcd.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@fpcd.com',
        password='admin123'  # Cambiar en producción
    )
    print('✅ Superusuario creado correctamente')
    print('   Email: admin@fpcd.com')
    print('   Password: admin123')
else:
    print('⚠️  El superusuario ya existe')
