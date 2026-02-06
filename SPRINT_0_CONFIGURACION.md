# 🚀 Sprint 0: Configuración del Entorno de Desarrollo

**Duración estimada:** 3-5 días  
**Objetivo:** Preparar todo el entorno de desarrollo para comenzar a programar

---

## ✅ Checklist de Tareas

### Tarea 1: Verificar Prerequisitos del Sistema
- [ ] Python 3.11+ instalado
- [ ] Docker y Docker Compose instalados
- [ ] Git instalado
- [ ] VS Code (o IDE preferido) instalado
- [ ] Navegador web moderno

### Tarea 2: Crear Estructura Base del Proyecto
- [ ] Crear estructura de carpetas
- [ ] Inicializar repositorio Git
- [ ] Crear archivo .gitignore

### Tarea 3: Configurar Entorno Virtual Python
- [ ] Crear entorno virtual
- [ ] Activar entorno virtual
- [ ] Crear archivo requirements.txt

### Tarea 4: Instalar Django y Dependencias
- [ ] Instalar Django
- [ ] Instalar dependencias adicionales
- [ ] Verificar instalación

### Tarea 5: Crear Proyecto Django
- [ ] Crear proyecto con estructura personalizada
- [ ] Configurar settings (base, development, production)
- [ ] Configurar variables de entorno

### Tarea 6: Configurar PostgreSQL con Docker
- [ ] Crear docker-compose.yml
- [ ] Levantar contenedor de PostgreSQL
- [ ] Verificar conexión a la base de datos

### Tarea 7: Configuración Inicial de Django
- [ ] Configurar base de datos en settings
- [ ] Ejecutar migraciones iniciales
- [ ] Crear superusuario
- [ ] Probar servidor de desarrollo

### Tarea 8: Configurar TailwindCSS
- [ ] Instalar Node.js y npm
- [ ] Configurar Tailwind en el proyecto
- [ ] Crear archivos de configuración

### Tarea 9: Estructura de Templates Base
- [ ] Crear carpeta templates
- [ ] Crear template base.html
- [ ] Configurar archivos estáticos

### Tarea 10: Control de Versiones
- [ ] Hacer commit inicial
- [ ] Crear branches principales (main, develop)
- [ ] Documentar convenciones de commits

---

## 📝 Pasos Detallados

### **PASO 1: Verificar Prerequisitos**

Ejecuta estos comandos en tu terminal para verificar:

```bash
# Verificar Python
python3 --version
# Debe mostrar: Python 3.11.x o superior

# Verificar Docker
docker --version
docker-compose --version

# Verificar Git
git --version

# Verificar Node.js (para Tailwind)
node --version
npm --version
```

Si falta algo, necesitarás instalarlo antes de continuar.

---

### **PASO 2: Crear Estructura Base del Proyecto**

```bash
# Ya estamos en /home/dw/workspace/FPCD
cd /home/dw/workspace/FPCD

# Crear estructura de carpetas
mkdir -p fpcd_project/{config/settings,apps,templates,static/{css,js,images},media,docker,requirements}

# Inicializar Git (si no está inicializado)
git init

# Crear .gitignore
```

Contenido del `.gitignore`:
```
# Python
*.py[cod]
*$py.class
__pycache__/
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static_root

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Node (para Tailwind)
node_modules/
package-lock.json
```

---

### **PASO 3: Configurar Entorno Virtual**

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate

# Verificar que estamos en el entorno virtual
which python
# Debe mostrar la ruta dentro de venv/
```

---

### **PASO 4: Crear Requirements**

Crear archivo `requirements/base.txt`:

```txt
# Django Core
Django==5.0.1
psycopg2-binary==2.9.9

# Django Extensions
django-environ==0.11.2
django-crispy-forms==2.1
crispy-tailwind==1.0.3

# Editor de texto
django-tinymce==4.0.0

# Tagging
django-taggit==5.0.1

# Image processing
Pillow==10.2.0

# Tasks & Email
celery==5.3.6
redis==5.0.1

# Utilities
python-slugify==8.0.1
```

Crear archivo `requirements/development.txt`:

```txt
-r base.txt

# Development tools
django-debug-toolbar==4.2.0
ipython==8.20.0
```

Crear archivo `requirements/production.txt`:

```txt
-r base.txt

# Production server
gunicorn==21.2.0

# Security
django-cors-headers==4.3.1
```

---

### **PASO 5: Instalar Dependencias**

```bash
# Instalar dependencias de desarrollo
pip install -r requirements/development.txt

# Verificar instalación
pip list | grep Django
```

---

### **PASO 6: Crear Proyecto Django**

```bash
# Crear proyecto Django en el directorio actual
django-admin startproject config fpcd_project

# La estructura quedará:
# fpcd_project/
#   ├── config/
#   │   ├── __init__.py
#   │   ├── settings.py  (lo dividiremos después)
#   │   ├── urls.py
#   │   ├── asgi.py
#   │   └── wsgi.py
#   └── manage.py
```

---

### **PASO 7: Configurar Docker para PostgreSQL**

Crear archivo `docker-compose.yml` en la raíz del proyecto:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: fpcd_postgres
    environment:
      POSTGRES_DB: fpcd_db
      POSTGRES_USER: fpcd_user
      POSTGRES_PASSWORD: fpcd_secure_password_2026
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - fpcd_network

  redis:
    image: redis:7-alpine
    container_name: fpcd_redis
    ports:
      - "6379:6379"
    networks:
      - fpcd_network

volumes:
  postgres_data:

networks:
  fpcd_network:
    driver: bridge
```

Levantar los contenedores:

```bash
docker-compose up -d

# Verificar que están corriendo
docker-compose ps
```

---

### **PASO 8: Configurar Variables de Entorno**

Crear archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=fpcd_db
DB_USER=fpcd_user
DB_PASSWORD=fpcd_secure_password_2026
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (configurar después)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

### **PASO 9: Dividir Settings de Django**

Crear estructura de settings:

1. Mover `config/settings.py` → `config/settings/base.py`
2. Crear `config/settings/development.py`
3. Crear `config/settings/production.py`
4. Crear `config/settings/__init__.py`

Contenido de `config/settings/base.py`: (configuración común)

Contenido de `config/settings/development.py`:
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1']
```

---

### **PASO 10: Ejecutar Migraciones Iniciales**

```bash
# Desde fpcd_project/
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
# Email: admin@fpcd.com
# Password: (elige una segura)

# Probar servidor
python manage.py runserver

# Abrir navegador en: http://localhost:8000
# Admin panel en: http://localhost:8000/admin
```

---

## ✅ Verificación Final

Al terminar el Sprint 0, debes poder:

- ✅ Ver la página de bienvenida de Django en http://localhost:8000
- ✅ Acceder al panel de administración en http://localhost:8000/admin
- ✅ Conectar a PostgreSQL (docker ps muestra el contenedor corriendo)
- ✅ Ver las migraciones aplicadas sin errores
- ✅ Entorno virtual activado y funcionando

---

## 🎯 Siguiente Paso

Una vez completado el Sprint 0, estaremos listos para comenzar el **Sprint 1: Sistema de Autenticación y Usuarios**.

---

## 📌 Notas Importantes

- **NO commitear el archivo .env** (debe estar en .gitignore)
- **Mantener el entorno virtual activado** mientras trabajas
- **Documentar cualquier problema** que encuentres
- **Los contenedores Docker** deben estar corriendo antes de iniciar el servidor Django

---

**Última actualización:** 6 de Febrero, 2026
