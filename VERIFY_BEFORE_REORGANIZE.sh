#!/bin/bash

################################################################################
#                                                                              #
#  PRE-REORGANIZACIÓN - Verificación y Validación                            #
#                                                                              #
#  Este script verifica que el proyecto está en buen estado antes de          #
#  ejecutar la reorganización.                                                #
#                                                                              #
#  USO: bash VERIFY_BEFORE_REORGANIZE.sh                                     #
#                                                                              #
################################################################################

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}\n"
}

print_ok() {
    echo -e "${GREEN}✓${NC} $1"
}

print_fail() {
    echo -e "${RED}✗${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

################################################################################

print_header "VERIFICACIÓN PRE-REORGANIZACIÓN"

errors=0
warnings=0

echo "Verificando requisitos previos..."
echo ""

# 1. Verificar directorio correcto
if [ -f "manage.py" ]; then
    print_ok "manage.py encontrado"
else
    print_fail "manage.py NO encontrado"
    errors=$((errors + 1))
fi

# 2. Verificar git
if [ -d ".git" ]; then
    print_ok "Repositorio git existe"
    
    # Verificar que está en main
    branch=$(git branch --show-current)
    if [ "$branch" = "main" ]; then
        print_ok "En rama: main"
    else
        print_warn "Rama actual: $branch (considerar estar en main)"
        warnings=$((warnings + 1))
    fi
    
    # Verificar cambios sin guardar
    changes=$(git status -s | wc -l)
    if [ $changes -eq 0 ]; then
        print_ok "Directorio limpio (sin cambios no guardados)"
    else
        print_warn "Hay $changes cambios sin guardar"
        git status -s | head -5
        if [ $changes -gt 5 ]; then
            echo "... y $(($changes - 5)) más"
        fi
        warnings=$((warnings + 1))
    fi
else
    print_fail "No es un repositorio git"
    errors=$((errors + 1))
fi

# 3. Verificar requisitos.txt
if [ -f "requirements.txt" ]; then
    print_ok "requirements.txt existe"
else
    print_fail "requirements.txt NO encontrado"
    errors=$((errors + 1))
fi

# 4. Verificar venv
if [ -d "venv" ]; then
    print_ok "venv/ existe"
else
    print_warn "venv/ no encontrada (considerar crearla)"
    warnings=$((warnings + 1))
fi

# 5. Verificar que las carpetas destino no existen
echo ""
echo "Verificando que las carpetas destino no existen..."
echo ""

conflicting_dirs=()

for dir in docs docker src scripts tests; do
    if [ -d "$dir" ]; then
        print_warn "$dir/ ya existe"
        warnings=$((warnings + 1))
        conflicting_dirs+=("$dir")
    else
        print_ok "$dir/ no existe (OK)"
    fi
done

# 6. Verificar archivos críticos
echo ""
echo "Verificando archivos críticos..."
echo ""

if [ -f "config/settings.py" ]; then
    print_ok "config/settings.py existe"
else
    print_fail "config/settings.py NO encontrado"
    errors=$((errors + 1))
fi

if [ -d "config" ]; then
    print_ok "config/ existe"
else
    print_fail "config/ NO encontrada"
    errors=$((errors + 1))
fi

# 7. Verificar apps
echo ""
echo "Verificando aplicaciones Django..."
echo ""

apps_found=0
for app in users devotionals materials newsletter; do
    if [ -d "$app" ]; then
        print_ok "$app/ encontrada"
        apps_found=$((apps_found + 1))
    else
        print_fail "$app/ NO encontrada"
        errors=$((errors + 1))
    fi
done

# 8. Verificar documentación
echo ""
echo "Verificando archivos de documentación..."
echo ""

md_files=$(find . -maxdepth 1 -name "*.md" -type f | wc -l)
echo -e "Se encontraron ${GREEN}$md_files${NC} archivos .md en raíz"

if [ $md_files -gt 5 ]; then
    print_ok "Documentación dispersa (este es el problema que se va a resolver)"
fi

# 9. Verificar Docker
echo ""
echo "Verificando archivos Docker..."
echo ""

docker_files_count=$(find . -maxdepth 1 -name "docker*" -o -name "Dockerfile" | grep -c . || true)
echo -e "Se encontraron ${GREEN}$docker_files_count${NC} archivos Docker en raíz"

# 10. Verificar Python
echo ""
echo "Verificando Python..."
echo ""

if command -v python3 &> /dev/null; then
    version=$(python3 --version)
    print_ok "$version instalado"
else
    print_fail "Python3 no encontrado"
    errors=$((errors + 1))
fi

# 11. Verificar que manage.py funciona
echo ""
echo "Verificando que Django está operativo..."
echo ""

if python manage.py check > /dev/null 2>&1; then
    print_ok "Django check pasado"
else
    print_warn "Django check falló (puede causar problemas)"
    warnings=$((warnings + 1))
fi

################################################################################
# RESUMEN
################################################################################

print_header "RESUMEN DE VERIFICACIÓN"

echo "Errores encontrados: ${RED}$errors${NC}"
echo "Advertencias encontradas: ${YELLOW}$warnings${NC}"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✓ VERIFICACIÓN COMPLETADA - Todo OK${NC}"
    echo ""
    echo "Puedes ejecutar la reorganización con:"
    echo "  bash REORGANIZE.sh"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠ VERIFICACIÓN CON ADVERTENCIAS${NC}"
    echo ""
    echo "La reorganización puede proceder, pero ten en cuenta:"
    echo "  - Cambios no guardados: considera hacer commit primero"
    echo "  - Rama: verifica estar en 'main' antes de proceder"
    echo "  - Django: algunos checks fallaron, pueden haber errores"
    echo ""
    read -p "¿Deseas proceder? (s/n): " response
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        echo ""
        echo "Ejecuta: bash REORGANIZE.sh"
    fi
    exit 0
else
    echo -e "${RED}✗ VERIFICACIÓN FALLÓ${NC}"
    echo ""
    echo "Corrige los errores antes de proceder:"
    if [ ! -f "manage.py" ]; then
        echo "  - Asegúrate de estar en el directorio raíz del proyecto"
    fi
    if [ ! -d ".git" ]; then
        echo "  - Inicializa git: git init"
    fi
    if [ ! -f "config/settings.py" ]; then
        echo "  - Asegúrate de que el proyecto Django está intacto"
    fi
    echo ""
    echo "Para más ayuda, revisa la documentación en docs/"
    exit 1
fi
