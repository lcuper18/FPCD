#!/bin/bash

################################################################################
#                                                                              #
#  SCRIPT DE REORGANIZACIÓN - Fe para Cada Día                               #
#                                                                              #
#  Este script reorganiza el proyecto a una estructura profesional            #
#  Crea: docs/, docker/, src/, scripts/, tests/, static/images/              #
#                                                                              #
#  USO: bash REORGANIZE.sh                                                    #
#  SEGURO: Hace backup con git antes de empezar                              #
#                                                                              #
################################################################################

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}\n"
}

print_step() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

confirm() {
    local prompt="$1"
    local response
    read -p "$(echo -e ${YELLOW}$prompt${NC}) (s/n): " response
    [[ "$response" == "s" || "$response" == "S" ]]
}

################################################################################
# PASO 0: VERIFICACIÓN INICIAL
################################################################################

print_header "PASO 0: VERIFICACIÓN INICIAL"

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "manage.py no encontrado. Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

print_step "Directorio correcto verificado"

# Verificar git
if [ ! -d ".git" ]; then
    print_error "No es un repositorio git"
    exit 1
fi

print_step "Git repository verificado"

# Mostrar estado actual
echo -e "${BLUE}Estado actual:${NC}"
echo -e "  Rama: $(git branch --show-current)"
echo -e "  Cambios no guardados: $(git status -s | wc -l)"

if [ $(git status -s | wc -l) -gt 0 ]; then
    print_warning "Hay cambios no guardados"
    confirm "¿Deseas hacer commit antes de continuar?" || exit 1
    
    git add .
    git commit -m "Backup antes de reorganización"
    print_step "Backup creado"
fi

################################################################################
# PASO 1: CONFIRMACIÓN FINAL
################################################################################

print_header "PASO 1: CONFIRMACIÓN"

cat << 'EOF'
Este script va a:

  ✓ Crear carpeta docs/ con documentación
  ✓ Crear carpeta docker/ con configuración Docker
  ✓ Crear carpeta src/ con las apps Django
  ✓ Crear carpeta scripts/ con utilidades
  ✓ Crear carpeta tests/ para tests
  ✓ Mover images/ a static/images/
  ✓ Actualizar config/settings.py
  ✓ Eliminar archivos duplicados
  ✓ Crear archivos auxiliares

Se puede deshacer con: git reset --hard HEAD~1
EOF

echo ""
confirm "¿Estás seguro de que quieres continuar?" || exit 1

################################################################################
# PASO 2: CREAR ESTRUCTURA DE CARPETAS
################################################################################

print_header "PASO 2: CREAR ESTRUCTURA DE CARPETAS"

# Crear carpetas
echo "Creando directorios..."
mkdir -p docs/{guides,dev-notes}
print_step "docs/ creada"

mkdir -p docker
print_step "docker/ creada"

mkdir -p src
print_step "src/ creada"

mkdir -p scripts
print_step "scripts/ creada"

mkdir -p tests
print_step "tests/ creada"

mkdir -p static/images
print_step "static/images/ creada"

mkdir -p .github
print_step ".github/ creada"

################################################################################
# PASO 3: MOVER DOCUMENTACIÓN
################################################################################

print_header "PASO 3: MOVER DOCUMENTACIÓN"

# Mover archivos .md principales a docs/
echo "Moviendo archivos de documentación..."
for file in README.md SETUP.md DEPLOYMENT.md DOCKER.md API.md ARCHITECTURE.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/ && print_step "Movido: $file → docs/"
    fi
done

# Mover guías específicas
echo "Moviendo guías..."
for file in QUICKSTART.md GITHUB_SETUP.md DOKPLOY.md PASOS_FECADADIA.md DOMINIO_FECADADIA.md VERIFICATION.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/guides/ && print_step "Movido: $file → docs/guides/"
    fi
done

# Mover notas de desarrollo
echo "Moviendo notas de desarrollo..."
for file in TRACKING.md TRACKING_v2.md CHECKLIST.md CHECKLIST_v2.md SUMMARY.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/dev-notes/ && print_step "Movido: $file → docs/dev-notes/"
    fi
done

# Eliminar duplicados en dev-notes
if [ -f "docs/dev-notes/TRACKING_v2.md" ]; then
    rm docs/dev-notes/TRACKING_v2.md
    print_step "Eliminado duplicado: TRACKING_v2.md"
fi

if [ -f "docs/dev-notes/CHECKLIST_v2.md" ]; then
    rm docs/dev-notes/CHECKLIST_v2.md
    print_step "Eliminado duplicado: CHECKLIST_v2.md"
fi

################################################################################
# PASO 4: MOVER CONFIGURACIÓN DOCKER
################################################################################

print_header "PASO 4: MOVER CONFIGURACIÓN DOCKER"

echo "Moviendo archivos Docker..."

if [ -f "Dockerfile" ]; then
    mv Dockerfile docker/
    print_step "Movido: Dockerfile → docker/"
fi

if [ -f "docker-compose.yml" ]; then
    mv docker-compose.yml docker/docker-compose.prod.yml
    print_step "Movido: docker-compose.yml → docker/docker-compose.prod.yml"
fi

if [ -f "docker-compose.dev.yml" ]; then
    mv docker-compose.dev.yml docker/
    print_step "Movido: docker-compose.dev.yml → docker/"
fi

if [ -f "docker-compose.sqlite.yml" ]; then
    mv docker-compose.sqlite.yml docker/docker-compose.dev.yml
    print_step "Movido: docker-compose.sqlite.yml → docker/docker-compose.dev.yml"
fi

if [ -f ".dockerignore" ]; then
    mv .dockerignore docker/
    print_step "Movido: .dockerignore → docker/"
fi

################################################################################
# PASO 5: REORGANIZAR APPS DJANGO
################################################################################

print_header "PASO 5: REORGANIZAR APPS DJANGO"

echo "Moviendo aplicaciones a src/..."

if [ -d "users" ]; then
    mv users src/
    print_step "Movido: users/ → src/"
fi

if [ -d "devotionals" ]; then
    mv devotionals src/
    print_step "Movido: devotionals/ → src/"
fi

if [ -d "materials" ]; then
    mv materials src/
    print_step "Movido: materials/ → src/"
fi

if [ -d "newsletter" ]; then
    mv newsletter src/
    print_step "Movido: newsletter/ → src/"
fi

# Crear __init__.py en src/
touch src/__init__.py
print_step "Creado: src/__init__.py"

################################################################################
# PASO 6: ORGANIZAR ASSETS
################################################################################

print_header "PASO 6: ORGANIZAR ASSETS"

echo "Moviendo imágenes..."

if [ -d "images" ]; then
    # Si hay archivos en images/, moverlos a static/images/
    if [ "$(ls -A images)" ]; then
        mv images/* static/images/
        print_step "Movidas imágenes → static/images/"
    fi
    rmdir images
    print_step "Eliminada carpeta images/"
fi

# Eliminar CSS duplicado
if [ -f "styles.css" ]; then
    rm styles.css
    print_step "Eliminado: styles.css (duplicado)"
fi

################################################################################
# PASO 7: MOVER SCRIPTS
################################################################################

print_header "PASO 7: MOVER SCRIPTS"

echo "Moviendo scripts..."

if [ -f "run.sh" ]; then
    mv run.sh scripts/
    print_step "Movido: run.sh → scripts/"
fi

if [ -f "setup.sh" ]; then
    mv setup.sh scripts/
    print_step "Movido: setup.sh → scripts/"
fi

################################################################################
# PASO 8: CREAR ARCHIVOS AUXILIARES
################################################################################

print_header "PASO 8: CREAR ARCHIVOS AUXILIARES"

# Crear .env.example si no existe
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'ENVEOF'
# Django Settings
DEBUG=False
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,fecadadia.com,www.fecadadia.com,148.230.92.233

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=fpcd_db
DB_USER=postgres
DB_PASSWORD=change-me
DB_HOST=db
DB_PORT=5432

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
ENVEOF
    print_step "Creado: .env.example"
else
    print_warning ".env.example ya existe"
fi

# Crear tests/__init__.py
touch tests/__init__.py
print_step "Creado: tests/__init__.py"

# Crear docs/README.md
cat > docs/README.md << 'DOCEOF'
# 📚 Documentación - Fe para Cada Día

Índice de documentación del proyecto.

## 📖 Documentación Principal

- [README.md](README.md) - Descripción general del proyecto
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura y diseño
- [SETUP.md](SETUP.md) - Configuración inicial
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de despliegue
- [DOCKER.md](DOCKER.md) - Guía Docker

## 📋 Guías Específicas

Ver carpeta `guides/`:

- [QUICKSTART.md](guides/QUICKSTART.md) - Inicio rápido en 5 minutos
- [GITHUB_SETUP.md](guides/GITHUB_SETUP.md) - Setup desde GitHub
- [DOKPLOY.md](guides/DOKPLOY.md) - Despliegue con Dokploy
- [DOMAIN_SETUP.md](guides/DOMAIN_SETUP.md) - Configuración del dominio
- [DNS_CONFIG.md](guides/DNS_CONFIG.md) - Configuración DNS
- [VERIFICATION.md](guides/VERIFICATION.md) - Verificación de setup

## 📝 Notas de Desarrollo

Ver carpeta `dev-notes/`:

- [TRACKING.md](dev-notes/TRACKING.md) - Histórico de trabajo
- [CHECKLIST.md](dev-notes/CHECKLIST.md) - Tareas completadas
- [SUMMARY.md](dev-notes/SUMMARY.md) - Resumen ejecutivo

---

**Última actualización**: $(date)
DOCEOF
    print_step "Creado: docs/README.md"

# Crear docker/README.md
cat > docker/README.md << 'DOCKEREOF'
# 🐳 Docker - Fe para Cada Día

Archivos de configuración Docker para desarrollo y producción.

## Archivos

- `Dockerfile` - Imagen Docker principal (Python 3.12)
- `docker-compose.prod.yml` - Composición para producción (PostgreSQL)
- `docker-compose.dev.yml` - Composición para desarrollo (SQLite)
- `.dockerignore` - Archivos a ignorar en la imagen

## Uso

### Desarrollo (SQLite)

```bash
docker-compose -f docker-compose.dev.yml up
```

### Producción (PostgreSQL)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Migraciones y datos

```bash
# Migraciones
docker-compose exec web python manage.py migrate

# Datos de prueba
docker-compose exec web python manage.py seed_data

# Crear superuser
docker-compose exec web python manage.py createsuperuser
```

---

**Nota**: Siempre ejecutar desde el directorio raíz del proyecto
DOCKEREOF
    print_step "Creado: docker/README.md"

# Crear .github/CONTRIBUTING.md
cat > .github/CONTRIBUTING.md << 'CONTRIBEOF'
# 🤝 Contribuciones - Fe para Cada Día

Gracias por tu interés en contribuir a este proyecto.

## Pasos para Contribuir

1. **Fork el repositorio**
2. **Crea una rama** (`git checkout -b feature/mi-feature`)
3. **Haz commits** (`git commit -am 'Add feature'`)
4. **Push a la rama** (`git push origin feature/mi-feature`)
5. **Abre Pull Request**

## Guías

- Consulta [ARCHITECTURE.md](../docs/ARCHITECTURE.md) para entender la estructura
- Lee [SETUP.md](../docs/SETUP.md) para configurar tu ambiente
- Revisa [CHECKLIST.md](../docs/dev-notes/CHECKLIST.md) de tareas completadas

---

¡Gracias por contribuir! 🎉
CONTRIBEOF
    print_step "Creado: .github/CONTRIBUTING.md"

################################################################################
# PASO 9: ACTUALIZAR CONFIGURACIÓN
################################################################################

print_header "PASO 9: ACTUALIZAR CONFIGURACIÓN"

echo "Actualizando config/settings.py..."

# Backup de settings.py
cp config/settings.py config/settings.py.backup
print_step "Backup creado: config/settings.py.backup"

# Actualizar INSTALLED_APPS
python3 << 'PYEOF'
import re

with open('config/settings.py', 'r') as f:
    content = f.read()

# Reemplazar en INSTALLED_APPS
replacements = [
    (r"'users'", "'src.users'"),
    (r"'devotionals'", "'src.devotionals'"),
    (r"'materials'", "'src.materials'"),
    (r"'newsletter'", "'src.newsletter'"),
]

for old, new in replacements:
    if re.search(old, content):
        content = re.sub(old, new, content)

with open('config/settings.py', 'w') as f:
    f.write(content)

print("✓ INSTALLED_APPS actualizado")
PYEOF

# Actualizar Dockerfile path si es necesario
if grep -q "Dockerfile" docker-compose.prod.yml 2>/dev/null; then
    sed -i 's|Dockerfile|./docker/Dockerfile|g' docker/docker-compose.prod.yml
    print_step "Actualizado: docker/docker-compose.prod.yml (path Dockerfile)"
fi

################################################################################
# PASO 10: ACTUALIZAR .GITIGNORE
################################################################################

print_header "PASO 10: ACTUALIZAR .GITIGNORE"

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'GITIGNEOF'
# Python
*.py[cod]
__pycache__/
*.so
*.egg
*.egg-info/
dist/
build/
.Python
env/
venv/
.env
*.pyc

# Django
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Backups
*.backup
*.bak

# Logs
*.log
logs/

# Cache
.cache/
.pytest_cache/

# Node modules (if using frontend)
node_modules/
GITIGNEOF
    print_step "Creado: .gitignore"
else
    # Verificar que db.sqlite3 está en .gitignore
    if ! grep -q "db.sqlite3" .gitignore; then
        echo "db.sqlite3" >> .gitignore
        print_step "Actualizado: .gitignore (agregado db.sqlite3)"
    else
        print_warning ".gitignore ya existe y contiene db.sqlite3"
    fi
fi

################################################################################
# PASO 11: VERIFICACIÓN
################################################################################

print_header "PASO 11: VERIFICACIÓN"

echo "Verificando estructura..."

# Verificar carpetas creadas
for dir in docs docker src scripts tests static/images .github; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/ existe"
    else
        echo -e "${RED}✗${NC} $dir/ FALTA"
    fi
done

# Verificar archivos principales
for file in manage.py config/settings.py requirements.txt; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file existe"
    else
        echo -e "${RED}✗${NC} $file FALTA"
    fi
done

# Verificar apps en src/
for app in users devotionals materials newsletter; do
    if [ -d "src/$app" ]; then
        echo -e "${GREEN}✓${NC} src/$app/ existe"
    else
        echo -e "${RED}✗${NC} src/$app/ FALTA"
    fi
done

################################################################################
# PASO 12: PROBAR DJANGO
################################################################################

print_header "PASO 12: PROBAR DJANGO"

echo "Ejecutando: python manage.py check"
if python manage.py check > /dev/null 2>&1; then
    print_step "Django check pasado ✓"
else
    print_error "Django check FALLÓ"
    echo -e "${YELLOW}Ejecuta: python manage.py check${NC}"
fi

################################################################################
# PASO 13: GIT COMMIT
################################################################################

print_header "PASO 13: GIT COMMIT"

echo "Preparando commit..."

# Stage todos los cambios
git add -A

# Mostrar cambios
echo -e "\n${BLUE}Cambios a ser commiteados:${NC}"
git status -s | head -20

if [ $(git status -s | wc -l) -gt 20 ]; then
    echo "... y $(( $(git status -s | wc -l) - 20 )) archivos más"
fi

echo ""
confirm "¿Deseas hacer commit con estos cambios?" || {
    print_warning "Cambios no commiteados. Puedes hacerlo manualmente con:"
    echo "  git add -A"
    echo "  git commit -m 'Reorganizar proyecto: estructura limpia y profesional'"
    exit 0
}

git commit -m "Reorganizar proyecto: estructura limpia y profesional

- Crear docs/ con toda la documentación
- Crear docker/ con configuración Docker
- Crear src/ con las apps Django
- Crear scripts/ con utilidades
- Crear tests/ para tests
- Mover images/ a static/images/
- Actualizar config/settings.py (INSTALLED_APPS)
- Eliminar archivos duplicados (styles.css, TRACKING_v2, CHECKLIST_v2)
- Crear archivos auxiliares (.env.example, README.md en carpetas)
- Actualizar .gitignore"

print_step "Commit realizado"

################################################################################
# RESUMEN FINAL
################################################################################

print_header "✨ REORGANIZACIÓN COMPLETADA"

cat << 'SUMMARYEOF'
El proyecto ha sido reorganizado exitosamente.

Nueva estructura:
  ├── README.md              (punto de entrada)
  ├── manage.py
  ├── requirements.txt
  ├── .env.example           (NUEVO)
  ├── .gitignore             (actualizado)
  ├── .github/               (NUEVO)
  ├── docs/                  (NUEVO - documentación)
  ├── docker/                (NUEVO - Docker)
  ├── config/
  ├── src/                   (NUEVO - apps Django)
  ├── templates/
  ├── static/
  ├── media/
  ├── tests/                 (NUEVO)
  ├── scripts/               (NUEVO)
  └── venv/

Próximos pasos:

  1. Prueba en local:
     docker-compose -f docker/docker-compose.dev.yml up

  2. Ejecuta migraciones:
     docker-compose exec web python manage.py migrate

  3. Genera datos de prueba:
     docker-compose exec web python manage.py seed_data

  4. Push a GitHub:
     git push origin main

¿Problemas? Puedes deshacer con:
  git reset --hard HEAD~1

SUMMARYEOF

print_step "¡Reorganización exitosa!"
