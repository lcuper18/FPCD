# 🏗️ Arquitectura Técnica - Plataforma de Enseñanza Bíblica

## Índice
1. [Diagrama de Arquitectura](#diagrama-de-arquitectura)
2. [Capa de Presentación](#capa-de-presentación)
3. [Capa de Aplicación](#capa-de-aplicación)
4. [Capa de Datos](#capa-de-datos)
5. [Seguridad](#seguridad)
6. [Escalabilidad](#escalabilidad)

---

## Diagrama de Arquitectura

### Vista de Alto Nivel

```
Internet
    │
    ▼
┌────────────────────────────────────────┐
│      Nginx (Reverse Proxy)             │
│  - Servir archivos estáticos           │
│  - SSL/TLS                             │
│  - Load Balancing (futuro)             │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│      Gunicorn (WSGI Server)            │
│  - Workers: 2-4                        │
│  - Timeout: 30s                        │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│      Django Application                │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  Middleware                      │ │
│  │  - Security                      │ │
│  │  - Authentication                │ │
│  │  - CSRF Protection               │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  Django Apps                     │ │
│  │  ├── accounts                    │ │
│  │  ├── content                     │ │
│  │  ├── workflow                    │ │
│  │  ├── media_manager               │ │
│  │  └── comments                    │ │
│  └──────────────────────────────────┘ │
└────────┬───────────────────┬───────────┘
         │                   │
         ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL     │  │  File Storage    │
│   (Docker)       │  │  - Media files   │
│                  │  │  - Static files  │
│  - Port: 5432    │  │                  │
│  - Volume: data/ │  │  (Local/S3)      │
└──────────────────┘  └──────────────────┘
```

---

## Capa de Presentación

### Templates (Django Template Language)

```
templates/
├── base.html                    # Template base
├── components/                  # Componentes reutilizables
│   ├── navbar.html
│   ├── footer.html
│   ├── sidebar.html
│   └── breadcrumbs.html
├── public/                      # Portal público
│   ├── home.html
│   ├── article_list.html
│   ├── article_detail.html
│   ├── category_list.html
│   └── search_results.html
├── dashboard/                   # Panel de usuarios
│   ├── dashboard.html
│   ├── my_content.html
│   └── create_content.html
└── admin/                       # Personalización admin
    └── custom_admin.html
```

### Diseño Responsive

- **Mobile First**: Diseño optimizado primero para móviles
- **Breakpoints**:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

### Framework CSS: TailwindCSS

**Ventajas**:
- Utility-first
- Fácil customización
- Tamaño optimizado
- Documentación excelente

**Alternativa**: Bootstrap 5
- Más componentes pre-diseñados
- Curva de aprendizaje más suave
- Mayor tamaño de archivo

---

## Capa de Aplicación

### Django Apps y Responsabilidades

#### 1. **accounts/** - Gestión de Usuarios

```python
# Modelos principales
- CustomUser (extiende AbstractUser)
  - role: CharField (admin, editor, reviewer)
  - bio: TextField
  - avatar: ImageField
  - created_at, updated_at

- UserProfile
  - user: OneToOne(CustomUser)
  - phone: CharField (optional)
  - location: CharField (optional)
  - social_links: JSONField
```

**Funcionalidades**:
- Registro y login
- Gestión de perfiles
- Recuperación de contraseña
- Cambio de rol (solo admin)

#### 2. **content/** - Gestión de Contenido

```python
# Modelos principales
- Category
  - name, slug
  - description
  - icon (optional)

- Tag
  - name, slug

- ContentBase (Abstract)
  - title, slug
  - author: FK(User)
  - content: TextField (rich text)
  - excerpt: TextField
  - featured_image: ImageField
  - status: CharField (draft, review, published, rejected)
  - categories: M2M(Category)
  - tags: M2M(Tag)
  - created_at, updated_at, published_at

- Article (hereda ContentBase)
  - reading_time: IntegerField

- Devotional (hereda ContentBase)
  - scripture_verse: CharField
  - scripture_reference: CharField

- BiblicalStudy (hereda ContentBase)
  - difficulty_level: CharField (beginner, intermediate, advanced)
  - scripture_references: JSONField

- BlogPost (hereda ContentBase)
  - (campos base son suficientes)
```

**Funcionalidades**:
- CRUD completo de contenido
- Filtrado por categoría, etiqueta, autor
- Búsqueda de texto completo
- Versionado (opcional)

#### 3. **media_manager/** - Gestión de Multimedia

```python
# Modelos principales
- Media
  - file: FileField
  - title: CharField
  - alt_text: CharField
  - uploaded_by: FK(User)
  - file_type: CharField (image, document)
  - file_size: IntegerField
  - created_at
```

**Funcionalidades**:
- Subida de archivos
- Validación (tipo, tamaño)
- Optimización de imágenes
- Biblioteca de medios
- Gestión de miniaturas

#### 4. **workflow/** - Flujo de Revisión

```python
# Modelos principales
- Review
  - content: FK(ContentBase)
  - reviewer: FK(User)
  - status: CharField (pending, approved, rejected)
  - comments: TextField
  - reviewed_at: DateTimeField

- ContentHistory (opcional)
  - content: FK(ContentBase)
  - changed_by: FK(User)
  - changes: JSONField
  - created_at
```

**Funcionalidades**:
- Envío a revisión
- Asignación de revisor
- Aprobación/Rechazo
- Comentarios de revisión
- Notificaciones

#### 5. **comments/** - Sistema de Comentarios

```python
# Modelos principales
- Comment
  - content_type: FK(ContentType)  # genérico
  - object_id: PositiveIntegerField
  - author: FK(User)
  - body: TextField
  - status: CharField (pending, approved, rejected)
  - parent: FK('self', null=True)  # respuestas
  - created_at, updated_at
```

**Funcionalidades** (100% completado):
- ✅ Modelo y migraciones
- ✅ Vistas de comentarios y moderación
- ✅ Templates
- ✅ Tests (13 tests)

#### 6. **newsletter/** - Newsletter y Suscripciones

```python
# Modelos principales
- Subscriber
  - email, first_name (unique)
  - is_active, is_verified
  - verification_token
  - subscribed_at, unsubscribed_at

- Newsletter
  - subject, content, content_html
  - status (draft, scheduled, sent, cancelled)
  - scheduled_for, sent_at
  - recipient_count, open_count, click_count
  - created_by

- NewsletterArchive
  - Archivo de boletines enviados
```

**Funcionalidades** (100% completado):
- ✅ Formulario de suscripción
- ✅ Modelo Subscriber con verificación
- ✅ Gestión de boletines
- ✅ Tests (8 tests)

#### 7. **analytics/** - Estadísticas y Visitas

```python
# Modelos principales
- PageView
  - content_type, object_id (GenericForeignKey)
  - user, session_key
  - ip_address, user_agent, referrer
  - viewed_at (con índices)

- DailyStats
  - date (unique)
  - total_views, unique_visitors
  - article_views, devotional_views, study_views, blog_views

- ContentStats
  - content_type, object_id (GenericForeignKey)
  - total_views, unique_views
  - last_viewed
```

**Funcionalidades** (100% completado):
- ✅ Middleware de tracking automático
- ✅ Estadísticas diarias agregadas
- ✅ Estadísticas por contenido
- ✅ Dashboard de estadísticas
- ✅ Tests (9 tests)

---

## Capa de Datos

### PostgreSQL - Configuración

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fpcd_db
      POSTGRES_USER: fpcd_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

### Índices Importantes

```sql
-- Índices para optimizar búsquedas
CREATE INDEX idx_content_status ON content_contentbase(status);
CREATE INDEX idx_content_author ON content_contentbase(author_id);
CREATE INDEX idx_content_published ON content_contentbase(published_at);
CREATE INDEX idx_content_slug ON content_contentbase(slug);

-- Índice de texto completo para búsqueda
CREATE INDEX idx_content_search ON content_contentbase 
USING GIN(to_tsvector('spanish', title || ' ' || content));
```

### Estrategia de Backup

- **Frecuencia**: Diaria (automática)
- **Retención**: 30 días
- **Comando**: `pg_dump fpcd_db > backup_$(date +%Y%m%d).sql`

---

## Seguridad

### Medidas Implementadas

1. **Autenticación**
   - Django authentication system
   - Contraseñas hasheadas (PBKDF2)
   - Login throttling

2. **Autorización**
   - Decoradores: `@login_required`, `@permission_required`
   - Permisos basados en roles
   - Validación a nivel de modelo

3. **Protección contra Ataques**
   - CSRF tokens en formularios
   - SQL Injection (Django ORM)
   - XSS (template auto-escaping)
   - Clickjacking protection

4. **Datos Sensibles**
   - Variables de entorno (.env)
   - Secret key segura
   - Credenciales de DB no en código

5. **HTTPS**
   - SSL/TLS en producción
   - HSTS headers
   - Secure cookies

### Configuración de Seguridad Django

```python
# settings/production.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

---

## Escalabilidad

### Estrategias de Crecimiento

#### Fase 1: Desarrollo (actual)
- 1 servidor
- PostgreSQL local (Docker)
- Almacenamiento local

#### Fase 2: Producción Inicial
- 1 servidor web
- PostgreSQL en contenedor dedicado
- CDN para archivos estáticos

#### Fase 3: Crecimiento
- Load balancer
- Múltiples servidores web
- PostgreSQL con réplicas
- Object Storage (S3)
- Redis para cache

### Optimizaciones

1. **Cache**
   - Django cache framework
   - Cache de templates
   - Cache de queries frecuentes

2. **Base de Datos**
   - Índices optimizados
   - Query optimization
   - Connection pooling

3. **Assets**
   - Minificación CSS/JS
   - Compresión de imágenes
   - Lazy loading

4. **Monitoreo**
   - Django Debug Toolbar (dev)
   - Logs estructurados
   - Métricas de rendimiento

---

## Decisiones Técnicas Clave

### ¿Por qué Django?
- ✅ Framework maduro y robusto
- ✅ Admin panel incorporado
- ✅ ORM potente
- ✅ Sistema de autenticación completo
- ✅ Gran comunidad y documentación

### ¿Por qué PostgreSQL?
- ✅ Base de datos relacional robusta
- ✅ Búsqueda de texto completo
- ✅ Tipos de datos avanzados (JSON)
- ✅ Excelente con Django

### ¿Por qué Docker?
- ✅ Portabilidad
- ✅ Aislamiento
- ✅ Fácil replicación de entornos
- ✅ Deployment simplificado

### ¿Por qué Redis + Celery?
- ✅ Tareas asíncronas (emails, newsletters)
- ✅ Ya configurado como broker en `base.py`
- ✅ Redis también usado como cache

### ¿Por qué Dokploy?
- ✅ Gestión de contenedores Docker en VPS propio
- ✅ SSL automático, dominios, backups
- ✅ URL: `https://platform.kooperlab.cloud/`

---

**Documento vivo - Última actualización: 24 de Marzo, 2026**
