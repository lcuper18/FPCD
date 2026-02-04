# 🔄 GUÍA DE REORGANIZACIÓN - Fe para Cada Día

## 📌 Resumen

Se han creado 3 scripts bash para reorganizar el proyecto de forma **segura y automatizada**:

1. **VERIFY_BEFORE_REORGANIZE.sh** - Verificar estado del proyecto
2. **REORGANIZE.sh** - Ejecutar la reorganización
3. **UNDO_REORGANIZE.sh** - Deshacer cambios si algo sale mal

---

## 🚀 PASOS PARA EJECUTAR

### Paso 1: Verificar Estado (Recomendado)

```bash
bash VERIFY_BEFORE_REORGANIZE.sh
```

Este script verifica:
- ✓ Que estamos en el directorio correcto (manage.py existe)
- ✓ Git repository está inicializado
- ✓ No hay cambios sin guardar
- ✓ Todas las apps Django están presentes
- ✓ Python y Django están operativos

**Salida esperada**:
```
✓ manage.py encontrado
✓ Repositorio git existe
✓ En rama: main
✓ Directorio limpio
✓ requirements.txt existe
... etc
```

### Paso 2: Ejecutar Reorganización

```bash
bash REORGANIZE.sh
```

Este script hará:

1. **Crear carpetas**
   - `docs/` con subcarpetas `guides/` y `dev-notes/`
   - `docker/` para configuración Docker
   - `src/` para aplicaciones Django
   - `scripts/` para utilidades
   - `tests/` para tests
   - `static/images/` para imágenes

2. **Mover archivos**
   - Documentación .md a `docs/`
   - Configuración Docker a `docker/`
   - Apps (users, devotionals, etc.) a `src/`
   - Scripts (run.sh, setup.sh) a `scripts/`
   - Imágenes a `static/images/`

3. **Actualizar configuración**
   - `config/settings.py` → INSTALLED_APPS actualizado
   - Crear `.env.example` (plantilla)
   - Actualizar `.gitignore`
   - Crear archivos README.md en carpetas

4. **Eliminar duplicados**
   - Borrar `styles.css` (duplicado)
   - Borrar `TRACKING_v2.md` (duplicado)
   - Borrar `CHECKLIST_v2.md` (duplicado)

5. **Git commit automático**
   - Hace commit con todos los cambios
   - Mensaje descriptivo incluido

---

## ⚠️ SEGURIDAD

### Antes de Reorganizar

El script te pedirá confirmación en varios puntos:

```
¿Estás seguro de que quieres continuar? (s/n): 
```

Responde `s` para continuar, `n` para cancelar.

### Backup Automático

El script hace backup automático:
- Antes de cambios, se crea commit con `git commit`
- Se crea copia de `config/settings.py` → `config/settings.py.backup`

### Deshacer Si Algo Sale Mal

Si algo no funciona, ejecuta:

```bash
bash UNDO_REORGANIZE.sh
```

Esto revierte el último commit (la reorganización) y todo vuelve al estado anterior.

---

## ✅ VERIFICACIÓN POST-REORGANIZACIÓN

Después de ejecutar el script, verifica:

### 1. Estructura de carpetas

```bash
ls -la
# Deberías ver: docs/, docker/, src/, scripts/, tests/
```

### 2. Django funciona

```bash
python manage.py check
# Salida: System check identified no issues (0 silenced).
```

### 3. Docker funciona

```bash
docker-compose -f docker/docker-compose.dev.yml --version
# Salida: Docker Compose version X.X.X
```

### 4. Tests ejecutan

```bash
python manage.py test
# Deberías ver cambios sin errores (puede ser OK si hay 0 tests)
```

---

## 📋 NUEVA ESTRUCTURA

Después de la reorganización, el proyecto se verá así:

```
fe_para_cada_dia/
├── README.md                    ← Punto de entrada
├── manage.py
├── requirements.txt
├── .env                         (no versionado)
├── .env.example                 ← NUEVO
├── .gitignore                   (actualizado)
│
├── .github/                     ← NUEVO
│   └── CONTRIBUTING.md          ← NUEVO
│
├── docs/                        ← NUEVO - Documentación centralizada
│   ├── README.md                ← Índice de docs
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── DEPLOYMENT.md
│   ├── DOCKER.md
│   ├── guides/                  ← Guías específicas
│   │   ├── QUICKSTART.md
│   │   ├── GITHUB_SETUP.md
│   │   ├── DOKPLOY.md
│   │   ├── DOMAIN_SETUP.md      (antes PASOS_FECADADIA.md)
│   │   ├── DNS_CONFIG.md        (antes DOMINIO_FECADADIA.md)
│   │   └── VERIFICATION.md
│   └── dev-notes/               ← Notas de desarrollo
│       ├── TRACKING.md
│       ├── CHECKLIST.md
│       └── SUMMARY.md
│
├── docker/                      ← NUEVO - Docker centralizado
│   ├── Dockerfile
│   ├── docker-compose.prod.yml  (antes docker-compose.yml)
│   ├── docker-compose.dev.yml   (antes docker-compose.sqlite.yml)
│   ├── .dockerignore
│   └── README.md                ← Guía Docker
│
├── config/
│   ├── settings.py              (UPDATED - INSTALLED_APPS)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── src/                         ← NUEVO - Apps Django
│   ├── users/
│   ├── devotionals/
│   ├── materials/
│   └── newsletter/
│
├── templates/
│   ├── base.html
│   ├── devotionals/
│   ├── materials/
│   ├── newsletter/
│   └── users/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/                  (movidas desde /images)
│
├── media/
│   └── (uploads de usuarios)
│
├── tests/                       ← NUEVO
│   └── __init__.py
│
├── scripts/                     ← NUEVO
│   ├── setup.sh                 (movido desde /)
│   ├── run.sh                   (movido desde /)
│   └── clean.sh
│
└── venv/                        (no versionado)
```

---

## 🔧 TROUBLESHOOTING

### Error: "manage.py no encontrado"

**Solución**: Asegúrate de estar en el directorio raíz del proyecto

```bash
cd /path/to/fe_para_cada_dia
bash REORGANIZE.sh
```

### Error: "No es un repositorio git"

**Solución**: Inicializa git primero

```bash
git init
git add .
git commit -m "Initial commit"
```

### Error: "Cambios sin guardar"

**Solución 1** - Guardar cambios:
```bash
git add .
git commit -m "Cambios en progreso"
```

**Solución 2** - Descartar cambios:
```bash
git checkout .
```

### Django check falla después de reorganización

**Solución**: Los imports en settings.py deben actualizarse manualmente si algo no funcionó:

```python
# config/settings.py
INSTALLED_APPS = [
    'src.users',           # Cambió de 'users' a 'src.users'
    'src.devotionals',
    'src.materials',
    'src.newsletter',
    # ...
]
```

### Docker compose no encuentra archivo

**Solución**: Los comandos deben ejecutarse desde la raíz:

```bash
# ❌ INCORRECTO
docker-compose -f docker-compose.dev.yml up

# ✅ CORRECTO
docker-compose -f docker/docker-compose.dev.yml up
```

---

## 📊 COMPARACIÓN: ANTES vs DESPUÉS

### Antes (Desordenado)
```
Raíz: 28+ items
  - 13 archivos .md
  - 4 archivos docker-*
  - styles.css (duplicado)
  - index.html (huérfano)
  - run.sh, setup.sh
  - ... mucho más
```

### Después (Limpio)
```
Raíz: 8 items
  - README.md
  - manage.py
  - requirements.txt
  - .env.example
  - .gitignore
  - .github/
  - docs/
  - docker/
  - config/
  - src/
  - templates/
  - static/
  - media/
  - tests/
  - scripts/
  - venv/
```

---

## 🎯 COMANDOS ÚTILES POST-REORGANIZACIÓN

### Desarrollo con Docker

```bash
# Iniciar (dev)
docker-compose -f docker/docker-compose.dev.yml up

# Migraciones
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate

# Datos de prueba
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py seed_data

# Parar
docker-compose -f docker/docker-compose.dev.yml down
```

### Ejecutar scripts

```bash
# Setup
bash scripts/setup.sh

# Run
bash scripts/run.sh

# Clean
bash scripts/clean.sh
```

### Git

```bash
# Ver cambios
git log --oneline | head -5

# Ver estructura
tree -L 2 -I '__pycache__|*.pyc|venv'
```

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Se pierden datos?**
R: No. Solo se reorganizan archivos. La base de datos (db.sqlite3) se mantiene fuera de git.

**P: ¿Cuánto tiempo toma?**
R: ~2-3 minutos en total (incluye confirmaciones interactivas).

**P: ¿Puedo deshacer?**
R: Sí. Ejecuta `bash UNDO_REORGANIZE.sh`

**P: ¿Qué pasa con el historial de git?**
R: Se crea un commit nuevo. El historial anterior se mantiene.

**P: ¿Necesito actualizar la documentación?**
R: No. Los archivos .md simplemente se mueven a `docs/`. Los enlaces internos se mantienen funcionales.

**P: ¿Y mi .env?**
R: Se mantiene igual. Se crea `.env.example` como plantilla.

---

## 📞 SOPORTE

Si algo no funciona:

1. **Revisa el error** - Léelo completamente
2. **Busca en TROUBLESHOOTING** - Arriba en este documento
3. **Deshaz y reinicia** - `bash UNDO_REORGANIZE.sh`
4. **Pide ayuda** - Comparte el error exacto

---

## ✨ SIGUIENTE PASO

Una vez reorganizado, puedes:

1. **Testear localmente** - `docker-compose -f docker/docker-compose.dev.yml up`
2. **Push a GitHub** - `git push origin main`
3. **Actualizar despliegue** - Actualizar referencias Docker en producción

---

**Creado**: 4 de Febrero 2026  
**Versión**: 1.0  
**Seguridad**: Alta - Reversible con git
