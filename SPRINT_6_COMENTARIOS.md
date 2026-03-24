# Sprint 6: Sistema de Comentarios ✅ COMPLETADO

**Período:** Marzo 24, 2026  
**Estado:** ✅ COMPLETADO  
**Commit:** `82ed6e8`

---

## 📋 Objetivos del Sprint

Implementar un sistema de comentarios completo para la plataforma FPCD:
- Comentarios en artículos y devocionales
- Respuestas anidadas (1 nivel)
- Sistema de moderación con roles
- Tests de vistas

---

## ✅ Tareas Completadas

### Modelos (Sprint anterior — incluido aquí por referencia)
- [x] `Comment` — contenido, autor, estado, IP, parent (respuestas), content_type/content_id
- [x] `CommentVote` — likes/dislikes por usuario
- [x] `CommentStatus` — PENDING, APPROVED, REJECTED, SPAM
- [x] Migración `0001_initial` aplicada

### Vistas (`apps/comments/views.py`)
- [x] `CommentListView` — lista paginada de comentarios aprobados
- [x] `CommentCreateView` — crea comentario (auth = auto-aprobado, anónimo = pendiente)
- [x] `ReplyCreateView` — respuesta a un comentario padre
- [x] `CommentVoteView` — like/dislike con toggle
- [x] `CommentApproveView` — aprueba comentario (revisor/admin)
- [x] `CommentRejectView` — rechaza comentario (revisor/admin)
- [x] `CommentModerationListView` — dashboard de moderación paginado con filtros

### URLs (`apps/comments/urls.py`)
- [x] `moderacion/` → `CommentModerationListView` (namespace: `comments:moderation`)
- [x] `reply/<int:parent_id>/` → `ReplyCreateView` (namespace: `comments:reply`)
- [x] `<str:content_type>/<int:content_id>/` → `CommentListView`
- [x] `<str:content_type>/<int:content_id>/create/` → `CommentCreateView`
- [x] `<int:pk>/vote/` → `CommentVoteView`
- [x] `<int:pk>/approve/` → `CommentApproveView`
- [x] `<int:pk>/reject/` → `CommentRejectView`
- [x] Orden correcto (reply antes del patrón genérico `<str>/<int>`)

### Config (`config/urls.py`)
- [x] Wired: `comentarios/` → `apps.comments.urls`
- [x] Health check endpoint `/health/`
- [x] Todas las apps conectadas: accounts, content, comments, workflow, media

### Templates
- [x] `templates/comments/comment_list.html` — partial con form de comentario + lista con respuestas
- [x] `templates/comments/form.html` — página standalone de formulario
- [x] `templates/comments/moderation.html` — dashboard con stats cards y AJAX approve/reject
- [x] `templates/public/article_detail.html` — **NUEVO** — detalle de artículo público con sección de comentarios
- [x] `templates/content/article_detail.html` — sección de comentarios añadida (dashboard)

### Vista Pública (`apps/content/views_public.py`)
- [x] `ArticleDetailView.get_context_data` pasa `article_comments` al template
- [x] Import `from apps.comments.models import Comment, CommentStatus`

### Tests (`apps/comments/tests/test_views.py`)
- [x] `CommentCreateViewTest` — 2 tests
  - Usuario autenticado puede crear comentario
  - Comentarios de usuarios autenticados se aprueban automáticamente
- [x] `ReplyCreateViewTest` — 2 tests
  - Responder requiere autenticación (→ 302/403)
  - Respuesta crea comentario hijo con parent correcto
- [x] `CommentModerationViewTest` — 5 tests
  - Moderación requiere login (→ 302)
  - Moderación requiere rol reviewer o admin (editor → 403)
  - Reviewer puede acceder a moderación
  - Admin puede acceder a moderación
  - Dashboard muestra conteo de pendientes en contexto
- [x] `CommentApproveRejectViewTest` — 4 tests
  - Aprobar requiere permiso adecuado (→ 403 sin rol)
  - Reviewer puede aprobar comentarios
  - Admin puede rechazar comentarios

**Total: 13 tests — 13/13 PASAN ✅**

---

## 🐛 Bugs encontrados y solucionados

1. **URL pattern shadowing**: `<str:content_type>/<int:content_id>/` capturaba `reply/<id>/` → solución: mover `reply/` antes del patrón genérico.
2. **Namespace `comments` no registrado**: `opencode` había sobreescrito `config/urls.py` sin la URL `/comentarios/`. Reescrito manualmente.
3. **`public/article_detail.html` inexistente**: template referenciado por `ArticleDetailView` pero nunca creado en Sprints anteriores. Creado desde cero con sección de comentarios.
4. **`article_comments` no en contexto**: `ArticleDetailView.get_context_data` no pasaba comentarios al template. Añadida query correcta.

---

## 📁 Archivos Modificados

```
fpcd_project/
├── config/
│   └── urls.py                              (modificado — agregado comentarios/)
├── apps/
│   ├── comments/
│   │   ├── views.py                         (modificado — CommentModerationListView)
│   │   ├── urls.py                          (modificado — orden y moderacion/)
│   │   └── tests/
│   │       └── test_views.py                (NUEVO — 13 tests)
│   └── content/
│       └── views_public.py                  (modificado — article_comments context)
└── templates/
    ├── comments/
    │   ├── form.html                         (NUEVO)
    │   └── moderation.html                   (NUEVO)
    ├── public/
    │   └── article_detail.html               (NUEVO)
    └── content/
        └── article_detail.html               (modificado — sección de comentarios)
```

---

## 🔗 URLs disponibles

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/comentarios/moderacion/` | CommentModerationListView | Dashboard de moderación |
| `/comentarios/reply/<id>/` | ReplyCreateView | Responder a comentario |
| `/comentarios/<type>/<id>/` | CommentListView | Listar comentarios |
| `/comentarios/<type>/<id>/create/` | CommentCreateView | Crear comentario |
| `/comentarios/<pk>/approve/` | CommentApproveView | Aprobar (revisor/admin) |
| `/comentarios/<pk>/reject/` | CommentRejectView | Rechazar (revisor/admin) |

---

## ➡️ Siguiente: Sprint 7 — Newsletter y Analytics

- Sistema de suscripción (`Subscriber` model)
- Formulario de signup en portal público
- Envío de newsletters con Celery + Redis
- Contador de visitas por artículo
- Dashboard de estadísticas para admins
