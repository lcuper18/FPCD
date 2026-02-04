#!/bin/bash

################################################################################
#                                                                              #
#  DESHACER REORGANIZACIÓN                                                   #
#                                                                              #
#  Este script revierte los cambios de la reorganización.                    #
#  Solo funciona si el commit fue hecho con git.                             #
#                                                                              #
#  USO: bash UNDO_REORGANIZE.sh                                              #
#                                                                              #
################################################################################

set -e

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

print_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

################################################################################

print_header "DESHACER REORGANIZACIÓN"

# Verificar que estamos en un git repo
if [ ! -d ".git" ]; then
    print_error "No es un repositorio git"
    exit 1
fi

# Mostrar último commit
echo "Último commit:"
git log --oneline -1
echo ""

# Verificar si el último commit es la reorganización
last_commit=$(git log --oneline -1 | grep -i "reorganiz" || true)
if [ -z "$last_commit" ]; then
    print_warn "El último commit no parece ser la reorganización"
fi

echo ""
read -p "$(echo -e ${YELLOW}¿Deshacer el último commit? (s/n):${NC}) " response

if [ "$response" != "s" ] && [ "$response" != "S" ]; then
    print_warn "Operación cancelada"
    exit 0
fi

# Hacer reset
echo ""
echo "Revirtiendo cambios..."

git reset --hard HEAD~1

if [ $? -eq 0 ]; then
    print_ok "Cambios revertidos exitosamente"
    print_ok "Directorio restaurado al estado anterior"
    echo ""
    echo "Los cambios de la reorganización han sido deshechados."
    echo "El proyecto está en el estado anterior al commit de reorganización."
else
    print_error "Error al revertir cambios"
    exit 1
fi
