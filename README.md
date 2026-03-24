# 📖 Plataforma de Enseñanza Bíblica (FPCD)

## Descripción

Plataforma web para compartir contenido educativo bíblico incluyendo artículos, devocionales, estudios bíblicos y blogs. Diseñada para ser simple, intuitiva y accesible para todos los usuarios.

## 🎯 Objetivo

Facilitar el aprendizaje y la reflexión espiritual a través de una plataforma moderna y fácil de usar, permitiendo a editores y revisores colaborar en la creación de contenido de calidad.

## 👥 Usuarios

- **Visitantes**: Acceso público a todo el contenido
- **Editores**: Creación y gestión de contenido
- **Revisores**: Revisión y aprobación de publicaciones
- **Administradores**: Gestión completa del sistema

## 🛠️ Tecnologías

- **Backend**: Django 5.0.1 (Python 3.12.3)
- **Base de Datos**: PostgreSQL 15-alpine (Docker)
- **Cache / Cola de tareas**: Redis 7-alpine + Celery 5.3.6
- **Frontend**: TailwindCSS (CDN), TinyMCE, Django Templates
- **Infraestructura**: Docker Compose, Gunicorn, Dokploy (deploy)
- **Otras libs**: django-taggit, crispy-forms + crispy-tailwind, django-environ

## 📁 Estructura del Proyecto

```
FPCD/
├── .env                          # Variables de entorno (no en Git)
├── .gitignore
├── docker-compose.yml            # PostgreSQL + Redis (dev) + web (prod)
├── Dockerfile                    # Imagen de producción
├── README.md
├── PLAN_DE_PROYECTO.md
├── ARQUITECTURA_TECNICA.md
├── SPRINT_0_RESUMEN.md
├── SPRINT_1_AUTENTICACION.md
├── venv/                         # Entorno virtual Python
└── fpcd_project/
    ├── manage.py
    ├── create_superuser.py
    ├── config/
    │   ├── settings/
    │   │   ├── base.py
    │   │   ├── development.py
    │   │   └── production.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── apps/
    │   ├── accounts/        # Autenticación, roles, perfiles
    │   ├── content/         # Artículos, devocionales, estudios, blogs
    │   ├── workflow/        # Flujo de revisión y notificaciones
    │   ├── media_manager/   # Gestión de archivos e imágenes
    │   └── comments/        # Sistema de comentarios
    ├── templates/
    ├── static/
    └── media/
```

## 🚀 Estado Actual

**Fecha**: Marzo 2026  
**Sprint activo**: 7 — Newsletter y Analytics

| Sprint | Descripción | Estado |
|--------|-------------|--------|
| 0 | Configuración del entorno | ✅ Completado |
| 1 | Autenticación y usuarios (63 tests) | ✅ Completado |
| 2 | Gestión de contenido (CRUD, TinyMCE, tags) | ✅ Completado |
| 3 | Flujo de revisión y notificaciones | ✅ Completado |
| 4 | Gestión de multimedia | ✅ Completado |
| 5 | Portal público (home, listados, búsqueda) | ✅ Completado |
| 6 | Comentarios (vistas, moderación, tests 13 ✅) | ✅ Completado |
| 7 | Newsletter y Analytics | 🔄 En progreso |
| 8 | Testing completo y deploy a Dokploy | ⏳ Pendiente |

## 💻 Acceso Local (Desarrollo)

```bash
# 1. Levantar base de datos y Redis
docker-compose up -d db redis

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Iniciar servidor
cd fpcd_project
python manage.py runserver
```

- **Portal público**: http://localhost:8000
- **Panel admin**: http://localhost:8000/admin
  - Usuario: `admin` | Contraseña: `admin123`

## 📚 Documentación

- [PLAN_DE_PROYECTO.md](PLAN_DE_PROYECTO.md) — Plan completo y requerimientos
- [ARQUITECTURA_TECNICA.md](ARQUITECTURA_TECNICA.md) — Arquitectura y decisiones técnicas
- [SPRINT_0_RESUMEN.md](SPRINT_0_RESUMEN.md) — Resumen Sprint 0
- [SPRINT_1_AUTENTICACION.md](SPRINT_1_AUTENTICACION.md) — Planificación Sprint 1

## 🚢 Deploy

Deploy vía **Dokploy** en `https://platform.kooperlab.cloud/`

---

**Proyecto en desarrollo activo — Marzo 2026**
