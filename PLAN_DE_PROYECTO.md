# Plan de Proyecto - Plataforma de Enseñanza Bíblica

## 📋 Información General del Proyecto

**Nombre del Proyecto:** Plataforma de Enseñanza Bíblica (FPCD)  
**Fecha de Inicio:** 6 de Febrero, 2026  
**Estado:** En desarrollo activo (Sprint 6)
**Tecnologías:** Django 5.0.1, PostgreSQL 15 (Docker), Redis 7, Celery, TailwindCSS, TinyMCE

---

## 🎯 FASE 1: DEFINICIÓN Y ALCANCE DEL PROYECTO

### 1.1 Visión del Proyecto
Crear una plataforma web intuitiva y accesible para compartir contenido bíblico educativo, facilitando el aprendizaje y la reflexión espiritual a través de diferentes tipos de contenido.

### 1.2 Objetivos Principales
- ✅ Proporcionar un portal web amigable para visitantes
- ✅ Permitir la publicación de artículos, devocionales, estudios bíblicos y blogs
- ✅ Implementar sistema de gestión de contenido con roles (Admin, Editor, Revisor)
- ✅ Gestionar multimedia (imágenes y archivos)
- ✅ Asegurar un diseño simple e intuitivo

### 1.3 Usuarios del Sistema

#### Visitantes (No Autenticados)
- Leer contenido publicado
- Buscar artículos y estudios
- Navegar por categorías

#### Editores (Autenticados)
- Crear y editar su propio contenido
- Enviar contenido para revisión
- Ver estadísticas de sus publicaciones

#### Revisores (Autenticados)
- Revisar contenido enviado
- Aprobar o rechazar publicaciones
- Sugerir cambios

#### Administradores (Autenticados)
- Gestión completa del sistema
- Administrar usuarios y roles
- Configuración del sitio
- Publicación directa sin revisión

---

## 📊 FASE 2: ANÁLISIS DE REQUERIMIENTOS

### 2.1 Requerimientos Funcionales

#### RF1: Gestión de Contenido
- **RF1.1** - Crear, editar, eliminar artículos
- **RF1.2** - Crear, editar, eliminar devocionales
- **RF1.3** - Crear, editar, eliminar estudios bíblicos
- **RF1.4** - Crear, editar, eliminar entradas de blog
- **RF1.5** - Sistema de categorías y etiquetas
- **RF1.6** - Buscador de contenido

#### RF2: Gestión de Usuarios y Roles
- **RF2.1** - Registro e inicio de sesión
- **RF2.2** - Asignación de roles (Admin, Editor, Revisor)
- **RF2.3** - Perfiles de usuario
- **RF2.4** - Gestión de permisos por rol

#### RF3: Flujo de Publicación
- **RF3.1** - Estados: Borrador, En Revisión, Publicado, Rechazado
- **RF3.2** - Notificaciones de cambio de estado
- **RF3.3** - Comentarios de revisión
- **RF3.4** - Historial de versiones

#### RF4: Gestión de Multimedia
- **RF4.1** - Subir imágenes (formatos: JPG, PNG, WebP)
- **RF4.2** - Subir archivos PDF
- **RF4.3** - Biblioteca de medios
- **RF4.4** - Optimización de imágenes

#### RF5: Portal Público
- **RF5.1** - Página de inicio con contenido destacado
- **RF5.2** - Listado de artículos por categoría
- **RF5.3** - Vista detallada de contenido
- **RF5.4** - Navegación intuitiva
- **RF5.5** - Diseño responsive (móvil, tablet, desktop)

#### RF6: Sistema de Comentarios
- **RF6.1** - Comentar en artículos (usuarios autenticados)
- **RF6.2** - Moderación de comentarios (revisores/admin)
- **RF6.3** - Responder a comentarios
- **RF6.4** - Notificación de nuevos comentarios

#### RF7: Newsletter y Suscripciones
- **RF7.1** - Formulario de suscripción
- **RF7.2** - Gestión de suscriptores
- **RF7.3** - Envío de boletines
- **RF7.4** - Desuscripción

#### RF8: Redes Sociales
- **RF8.1** - Botones de compartir (Facebook, Twitter, WhatsApp)
- **RF8.2** - Meta tags para preview social
- **RF8.3** - Open Graph tags

#### RF9: Estadísticas
- **RF9.1** - Contador de visitas por artículo
- **RF9.2** - Dashboard de estadísticas para autores
- **RF9.3** - Artículos más leídos
- **RF9.4** - Reportes básicos para administradores

### 2.2 Requerimientos No Funcionales

- **RNF1 - Rendimiento:** Tiempo de carga < 3 segundos
- **RNF2 - Seguridad:** Autenticación segura, protección CSRF
- **RNF3 - Escalabilidad:** Soportar crecimiento de contenido
- **RNF4 - Usabilidad:** Interface intuitiva, accesibilidad WCAG 2.1
- **RNF5 - Mantenibilidad:** Código limpio, documentado
- **RNF6 - Compatibilidad:** Navegadores modernos (Chrome, Firefox, Safari, Edge)

---

## 🏗️ FASE 3: DISEÑO DE LA ARQUITECTURA

### 3.1 Arquitectura Técnica

```
┌─────────────────────────────────────────────┐
│           NAVEGADOR DEL USUARIO             │
└──────────────────┬──────────────────────────┘
                   │ HTTP/HTTPS
                   ▼
┌─────────────────────────────────────────────┐
│          SERVIDOR NGINX (Producción)        │
│              Static Files                   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         APLICACIÓN DJANGO                   │
│  ┌──────────────────────────────────────┐   │
│  │  Apps:                               │   │
│  │  - accounts (usuarios/auth)          │   │
│  │  - content (artículos, blog, etc)    │   │
│  │  - media (imágenes, archivos)        │   │
│  │  - workflow (revisión)               │   │
│  └──────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL     │  │  Media Storage   │
│   (Docker)       │  │  (Local/S3)      │
└──────────────────┘  └──────────────────┘
```

### 3.2 Estructura del Proyecto Django

```
fpcd_project/
├── config/                  # Configuración principal
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/           # Gestión de usuarios
│   ├── content/            # Contenido (artículos, etc)
│   ├── media_manager/      # Gestión de archivos
│   ├── workflow/           # Flujo de revisión
│   ├── comments/           # Sistema de comentarios
│   ├── newsletter/         # Newsletter y suscripciones
│   └── analytics/          # Estadísticas y visitas
├── templates/              # Plantillas HTML
├── static/                 # CSS, JS, imágenes estáticas
├── media/                  # Archivos subidos
├── docker/                 # Configuración Docker
├── requirements/           # Dependencias Python
└── manage.py
```

### 3.3 Modelos de Datos Principales

#### Usuario (accounts)
- Extiende AbstractUser de Django
- Roles: Admin, Editor, Revisor
- Perfil con biografía y foto

#### Contenido Base (content)
- Título, slug, contenido
- Autor, fecha creación/actualización
- Estado (borrador, revisión, publicado)
- Categorías, etiquetas
- Imagen destacada

#### Tipos de Contenido:
- Artículo
- Devocional (+ versículo del día)
- Estudio Bíblico (+ referencias bíblicas)
- Entrada de Blog

#### Revisión (workflow)
- Contenido, revisor
- Estado, comentarios
- Fecha de revisión

---

## 📅 FASE 4: CRONOGRAMA Y METODOLOGÍA

### 4.1 Metodología de Trabajo

Utilizaremos un enfoque **iterativo e incremental**, dividiendo el desarrollo en sprints de 1-2 semanas.

### 4.2 Cronograma Estimado

#### **Sprint 0: Preparación del Entorno ✅ COMPLETADO (Feb 6, 2026)**
- Configuración del entorno de desarrollo
- Instalación de Django y dependencias
- Configuración de Docker para PostgreSQL
- Estructura inicial del proyecto
- Control de versiones (Git)

#### **Sprint 1: Base del Proyecto ✅ COMPLETADO**
- CustomUser con email login, 3 roles
- Panel de administración
- Templates base (layout, navbar, footer)
- 13 vistas, 7 formularios, 63 tests unitarios

#### **Sprint 2: Gestión de Contenido ✅ COMPLETADO**
- Modelos: Artículo, Devocional, EstudioBiblico, BlogPost, Category
- CRUD completo de contenido para editores
- Sistema de categorías y etiquetas (django-taggit)
- Editor de texto enriquecido TinyMCE

#### **Sprint 3: Flujo de Revisión ✅ COMPLETADO**
- Estaós de publicación
- Sistema de revisión (Review, ContentSubmission)
- Notificaciones automáticas
- Dashboard para revisores

#### **Sprint 4: Gestión de Multimedia ✅ COMPLETADO**
- Subida de imágenes y archivos
- Biblioteca de medios con vista grid
- MediaFile, MediaFolder con metadatos

#### **Sprint 5: Portal Público ✅ COMPLETADO**
- Página de inicio
- Listados de contenido por tipo y categoría
- Vista de detalle
- Buscador
- Diseño responsive con TailwindCSS

#### **Sprint 6: Funcionalidades Sociales 🔄 EN PROGRESO (50%)**
- ✅ Modelo Comment + migraciones
- ⏳ Vistas y templates de comentarios
- ⏳ Moderación de comentarios
- ⏳ Tests

#### **Sprint 7: Newsletter y Estadísticas ⏳ PENDIENTE**
- Sistema de suscripción
- Envío de newsletters con Celery
- Contador de visitas
- Dashboard de estadísticas

#### **Sprint 8: Pulido y Testing ⏳ PENDIENTE**
- Suite completa de tests
- Corrección de bugs
- Optimización de rendimiento
- Deploy a Dokploy (https://platform.kooperlab.cloud/)

**DURACIÓN TOTAL ESTIMADA: 10-16 semanas**

---

## 🛠️ FASE 5: TECNOLOGÍAS Y HERRAMIENTAS

### 5.1 Backend
- **Python 3.11+**
- **Django 5.0+**
- **PostgreSQL 15+** (en Docker)
- **Pillow** (procesamiento de imágenes)
- **django-tinymce** (editor de texto enriquecido)
- **django-taggit** (sistema de etiquetas)
- **django-crispy-forms** (formularios mejorados)
- **Celery** (tareas asíncronas para emails)
- **Redis** (broker para Celery y cache)

### 5.2 Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla o Alpine.js para interactividad)**
- **TailwindCSS o Bootstrap 5** (framework CSS)
- **Django Templates**

### 5.3 Infraestructura
- **Docker & Docker Compose**
- **Git** (control de versiones)
- **GitHub/GitLab** (repositorio)
- **Nginx** (servidor web en producción)
- **Gunicorn** (servidor WSGI)

### 5.4 Herramientas de Desarrollo
- **VS Code** (IDE)
- **pgAdmin** (gestión de base de datos)
- **Postman** (testing de APIs si aplica)

---

## ✅ FASE 6: CRITERIOS DE ÉXITO

### Criterios Técnicos
- ✅ Sistema desplegado y funcional
- ✅ Base de datos correctamente estructurada
- ✅ Código limpio y documentado
- ✅ Tests básicos implementados
- ✅ Sin errores críticos

### Criterios Funcionales
- ✅ Los 3 roles pueden realizar sus funciones
- ✅ Flujo de publicación funciona correctamente
- ✅ Visitantes pueden navegar el contenido fácilmente
- ✅ Multimedia se gestiona correctamente
- ✅ Diseño responsive en todos los dispositivos

### Criterios de Usabilidad
- ✅ Interface intuitiva y fácil de usar
- ✅ Tiempo de carga aceptable
- ✅ Accesible desde diferentes dispositivos

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

1. **Revisar y aprobar este plan** ✋
2. **Configurar entorno de desarrollo** (Sprint 0)
3. **Iniciar desarrollo del Sprint 1**

---

## 📝 NOTAS Y CONSIDERACIONES

### Decisiones Tomadas ✅
- [x] **Sistema de comentarios en artículos**: SÍ - Los visitantes podrán comentar
- [x] **Tipo de autenticación**: Email (login con correo electrónico)
- [x] **Newsletter/Suscripciones**: SÍ - Sistema de suscripción por email
- [x] **Integración con redes sociales**: SÍ - Botones para compartir (Facebook, Twitter, WhatsApp)
- [x] **Analytics/Estadísticas**: SÍ - Contador de visitas por artículo
- [x] **Editor de texto**: TinyMCE (amigable e intuitivo)
- [x] **Framework CSS**: TailwindCSS (moderno y flexible)

### Riesgos Identificados
- **Riesgo:** Complejidad del editor de texto enriquecido
  - **Mitigación:** Usar soluciones probadas (TinyMCE, CKEditor)
  
- **Riesgo:** Gestión de archivos grandes
  - **Mitigación:** Límites de tamaño, optimización automática

- **Riesgo:** Seguridad en la autenticación
  - **Mitigación:** Usar sistema de Django, buenas prácticas

---

**Última actualización:** 24 de Marzo, 2026
