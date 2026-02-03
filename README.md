# Fe para Cada Día - Proyecto Django Completo

## 🙏 Descripción

**Fe para Cada Día** es una aplicación web cristiana desarrollada en Django que permite:

- 📖 Publicar y leer devocionales diarios
- 👥 Registro y autenticación de usuarios
- 💌 Suscripción a newsletter
- 🎯 Búsqueda de contenido por tema y categorías
- 💬 Sistema de comentarios
- ❤️ Favoritos de usuarios
- 📚 Biblioteca de materiales cristianos
- 🎨 Dashboard para colaboradores
- 🔐 Panel administrativo completo

---

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
./setup.sh
```

### Opción 2: Manual

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus configuraciones

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

Visita: **http://localhost:8000**

---

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- Git (opcional)

---

## 🗂️ Estructura del Proyecto

```
fe_para_cada_dia/
│
├── config/                 # Configuración principal Django
│   ├── settings.py        # Configuraciones
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI para producción
│
├── users/                 # App de usuarios
│   ├── models.py         # Modelo CustomUser
│   ├── forms.py          # Formularios de registro/login
│   ├── views.py          # Vistas de autenticación
│   └── admin.py          # Admin de usuarios
│
├── devotionals/          # App de devocionales
│   ├── models.py        # Devotional, Category, Comment, Favorite
│   ├── views.py         # Vistas de devocionales
│   ├── urls.py          # URLs de devocionales
│   └── admin.py         # Admin de devocionales
│
├── newsletter/          # App de newsletter
│   ├── models.py       # Subscriber, NewsletterCampaign
│   ├── views.py        # Suscripción
│   └── admin.py        # Admin de newsletter
│
├── materials/          # App de materiales
│   ├── models.py      # Material (estudios, guías, etc.)
│   ├── views.py       # Lista y detalle de materiales
│   └── admin.py       # Admin de materiales
│
├── templates/         # Plantillas HTML
│   ├── base.html     # Template base
│   ├── devotionals/  # Templates de devocionales
│   ├── users/        # Templates de usuarios
│   └── newsletter/   # Templates de newsletter
│
├── static/           # Archivos estáticos
│   ├── css/         # Estilos CSS
│   ├── js/          # JavaScript
│   └── img/         # Imágenes
│
├── media/           # Archivos subidos por usuarios
│
├── requirements.txt # Dependencias Python
├── manage.py       # Script de gestión Django
├── setup.sh        # Script de instalación automática
├── .env.example    # Ejemplo de variables de entorno
├── .gitignore      # Archivos ignorados por Git
└── DEPLOYMENT.md   # Guía de despliegue en Hostinger
```

---

## 🎨 Funcionalidades Principales

### 1. **Sistema de Usuarios**

- Registro con email único
- Login/Logout
- Perfiles de usuario editables
- Roles: Lector, Colaborador, Administrador
- Suscripción automática al newsletter (opcional)

### 2. **Devocionales**

- Devocional del día en la página principal
- Versículo bíblico destacado
- Contenido con editor rico (CKEditor)
- Reflexiones y oraciones
- Sistema de categorías y tags
- Búsqueda por tema, fecha, categoría
- Contador de vistas
- Sistema de favoritos

### 3. **Comentarios**

- Usuarios autenticados pueden comentar
- Moderación de comentarios por admin
- Aprobación manual antes de publicar

### 4. **Newsletter**

- Suscripción independiente (no requiere cuenta)
- Vinculación automática con usuarios registrados
- Gestión de campañas desde el admin
- Cancelación de suscripción

### 5. **Materiales**

- Biblioteca de recursos cristianos
- Tipos: Estudios, Guías, Artículos, Videos, Audios, E-books
- Archivos descargables
- Enlaces a recursos externos (YouTube, Drive)
- Búsqueda y filtros por tipo y categoría

### 6. **Dashboard para Colaboradores**

- Acceso rápido a funciones de creación
- Estadísticas básicas
- Enlaces directos al admin de Django

### 7. **Panel Administrativo**

- Django Admin personalizado
- Gestión completa de contenido
- Moderación de comentarios
- Gestión de usuarios y permisos
- Estadísticas de vistas y descargas

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Django
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=fe_para_cada_dia_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Sitio
SITE_NAME=Fe para Cada Día
YOUTUBE_CHANNEL_URL=https://youtube.com/@tucanal
```

---

## 📱 Responsive Design

- ✅ Bootstrap 5
- ✅ Mobile-first
- ✅ Diseño adaptativo para tablets y móviles
- ✅ Iconos con Bootstrap Icons

---

## 🎨 Personalización

### Cambiar colores

Edita `static/css/main.css`:

```css
:root {
    --primary-color: #4A90E2;    /* Azul */
    --secondary-color: #6B9F7F;  /* Verde */
    --accent-color: #D4AF37;     /* Dorado */
}
```

### Cambiar fuentes

Edita en `templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=TuFuente&display=swap" rel="stylesheet">
```

---

## 🚀 Deployment

Consulta **DEPLOYMENT.md** para instrucciones detalladas de despliegue en:
- Hostinger
- VPS
- Heroku
- PythonAnywhere

---

## 🛡️ Seguridad

- ✅ CSRF Protection
- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Validación de formularios
- ✅ SQL Injection protection (ORM Django)
- ✅ XSS Protection
- ✅ Configuración HTTPS para producción

---

## 📦 Dependencias Principales

- **Django 5.0.2** - Framework web
- **psycopg2-binary** - Adaptador PostgreSQL
- **Pillow** - Procesamiento de imágenes
- **django-ckeditor** - Editor de texto rico
- **django-crispy-forms** - Formularios bonitos
- **gunicorn** - Servidor WSGI para producción
- **whitenoise** - Servir archivos estáticos

---

## 🤝 Contribuir

Este proyecto es de código abierto para la gloria de Dios. Si deseas contribuir:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 Soporte

- **Email**: admin@feparacadadia.com
- **Documentación**: Lee este README y DEPLOYMENT.md
- **Issues**: Reporta problemas en GitHub

---

## 📄 Licencia

Este proyecto se distribuye de forma gratuita para uso en ministerios cristianos.

---

## 🙌 Créditos

Desarrollado con amor y dedicación para:
- Inspirar fe
- Edificar vidas
- Compartir el amor de Cristo

---

## 📖 Versículo

> *"Toda la Escritura es inspirada por Dios y útil para enseñar, para reprender, para corregir y para instruir en la justicia, a fin de que el siervo de Dios esté enteramente capacitado para toda buena obra."*
> 
> **— 2 Timoteo 3:16-17**

---

**Hecho con ❤️ para la gloria de Dios | Fe para Cada Día © 2026**
