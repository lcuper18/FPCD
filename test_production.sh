#!/bin/bash

###############################################################################
# 🧪 SCRIPT DE PRUEBAS EN PRODUCCIÓN - Fe para Cada Día
#
# Este script verifica que todo funciona correctamente en fecadadia.com
# después del despliegue
#
# Uso: bash test_production.sh
###############################################################################

set -e

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="fecadadia.com"
ADMIN_USER="admin_prod"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🧪 PRUEBAS DE PRODUCCIÓN - Fe para Cada Día                  ║"
echo "║     Dominio: $DOMAIN"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Variables para contar resultados
TESTS_PASSED=0
TESTS_FAILED=0

# Función para ejecutar pruebas
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"
    
    echo -n "🧪 $test_name... "
    
    if eval "$test_command" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Función para verificar headers
check_header() {
    local header_name="$1"
    local url="$2"
    
    echo -n "🧪 Verificando header: $header_name... "
    
    if curl -s -I "$url" 2>/dev/null | grep -i "^$header_name" > /dev/null; then
        echo -e "${GREEN}✓ Presente${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Ausente${NC}"
        ((TESTS_FAILED++))
    fi
}

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 1: CONECTIVIDAD HTTPS${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

run_test "HTTPS accesible" "curl -s -I https://$DOMAIN" "HTTP/1.1 200"
check_header "Server" "https://$DOMAIN"
check_header "Content-Type" "https://$DOMAIN"

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 2: SSL/TLS${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -n "🧪 Certificado SSL válido... "
if curl -s https://$DOMAIN -o /dev/null -w "%{http_code}" 2>/dev/null | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "🧪 SSL Certificate Info... "
if openssl s_client -connect $DOMAIN:443 -servername $DOMAIN </dev/null 2>/dev/null | grep -q "subject="; then
    echo -e "${GREEN}✓ Válido${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ No disponible${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 3: ADMIN PANEL${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

run_test "Admin accesible" "curl -s -I https://$DOMAIN/admin/" "HTTP/1.1 200\|HTTP/1.1 302"
run_test "Admin login page" "curl -s https://$DOMAIN/admin/ | head -50" "Django"

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 4: STATIC FILES${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

run_test "CSS Admin" "curl -s -I https://$DOMAIN/static/admin/css/base.css" "HTTP/1.1 200"
run_test "JavaScript Admin" "curl -s -I https://$DOMAIN/static/admin/js/core.js" "HTTP/1.1 200"
run_test "Bootstrap CSS" "curl -s -I https://$DOMAIN/static/css/" "HTTP/1.1"

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 5: URLS PRINCIPALES${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

run_test "Home page" "curl -s https://$DOMAIN/ | head -50" "<!DOCTYPE\|<html"
run_test "Admin site" "curl -s https://$DOMAIN/admin/ | head -20" "Django\|admin"

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRUEBA 6: HEADERS DE SEGURIDAD${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

check_header "Server" "https://$DOMAIN"
check_header "X-Frame-Options\|Content-Security-Policy" "https://$DOMAIN"

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}RESUMEN DE PRUEBAS${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo ""
echo -e "Total Tests: $(($TESTS_PASSED + $TESTS_FAILED))"
echo -e "${GREEN}✓ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}✗ Failed: $TESTS_FAILED${NC}"

echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ TODAS LAS PRUEBAS PASARON - SITIO FUNCIONANDO CORRECTAMENTE  ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🎉 Fe para Cada Día está lista en: https://$DOMAIN"
    echo ""
    echo "📝 Próximos pasos:"
    echo "   1. Accede a /admin/ e inicia sesión"
    echo "   2. Cambia la contraseña del admin"
    echo "   3. Crea contenido (devocionales, categorías, etc)"
    echo "   4. Configura y prueba email"
    echo "   5. Monitoriza en Dokploy dashboard"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ⚠️  ALGUNAS PRUEBAS FALLARON - REVISAR CONFIGURACIÓN           ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "💡 Soluciones:"
    echo "   1. Verifica que Dokploy está corriendo"
    echo "   2. Revisa logs en Dokploy dashboard"
    echo "   3. Verifica variables de entorno"
    echo "   4. Espera 5 minutos más si es primer despliegue"
    exit 1
fi
