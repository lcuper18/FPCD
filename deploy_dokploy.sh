#!/bin/bash

###############################################################################
# 🚀 SCRIPT AUTOMÁTICO DE DESPLIEGUE EN DOKPLOY
# 
# Este script automatiza el despliegue de Fe para Cada Día en Dokploy
# 
# Uso: bash deploy_dokploy.sh
###############################################################################

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚀 DESPLIEGUE AUTOMÁTICO EN DOKPLOY - Fe para Cada Día       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
DOKPLOY_IP="${DOKPLOY_IP:-148.230.92.233}"
DOKPLOY_PORT="${DOKPLOY_PORT:-3000}"
VPS_IP="${VPS_IP:-148.230.92.233}"
VPS_USER="${VPS_USER:-root}"
GITHUB_REPO="lcuper18/FPCD"
GITHUB_BRANCH="main"
PROJECT_NAME="Fe para Cada Día"
DOMAIN="fecadadia.com"

echo -e "${BLUE}ℹ️  Información de Despliegue:${NC}"
echo "   VPS IP: $VPS_IP"
echo "   Dokploy: http://$DOKPLOY_IP:$DOKPLOY_PORT"
echo "   GitHub Repo: $GITHUB_REPO"
echo "   Rama: $GITHUB_BRANCH"
echo "   Dominio: $DOMAIN"
echo ""

# Verificar SSH access
echo -e "${YELLOW}📌 PASO 1: Verificando acceso al VPS${NC}"
if ssh -o ConnectTimeout=5 $VPS_USER@$VPS_IP "echo 'SSH OK'" &>/dev/null; then
    echo -e "${GREEN}✓ Acceso SSH confirmado${NC}"
else
    echo -e "${RED}✗ No se puede conectar a $VPS_USER@$VPS_IP${NC}"
    echo "Verifica:"
    echo "  - IP correcta (actual: $VPS_IP)"
    echo "  - SSH keys configuradas"
    echo "  - Firewall permite puerto 22"
    exit 1
fi
echo ""

# Verificar Dokploy disponible
echo -e "${YELLOW}📌 PASO 2: Verificando Dokploy disponible${NC}"
if timeout 3 bash -c "cat < /dev/null > /dev/tcp/$DOKPLOY_IP/$DOKPLOY_PORT" 2>/dev/null; then
    echo -e "${GREEN}✓ Dokploy accesible en http://$DOKPLOY_IP:$DOKPLOY_PORT${NC}"
else
    echo -e "${RED}✗ Dokploy no accesible en http://$DOKPLOY_IP:$DOKPLOY_PORT${NC}"
    echo "Verifica que Dokploy esté corriendo en el VPS"
    exit 1
fi
echo ""

# Verificar repositorio GitHub
echo -e "${YELLOW}📌 PASO 3: Verificando repositorio GitHub${NC}"
if curl -s "https://api.github.com/repos/$GITHUB_REPO" | grep -q '"name"'; then
    echo -e "${GREEN}✓ Repositorio GitHub accesible${NC}"
else
    echo -e "${RED}✗ No se puede acceder a $GITHUB_REPO${NC}"
    exit 1
fi
echo ""

# Leer variables de entorno
echo -e "${YELLOW}📌 PASO 4: Configurando variables de entorno${NC}"
echo "Necesitamos algunas variables. Presiona Enter para usar el valor por defecto."
echo ""

read -p "SECRET_KEY (django-insecure-...): " SECRET_KEY
SECRET_KEY="${SECRET_KEY:-django-insecure-CAMBIAR-EN-PRODUCCION}"

read -p "DB_PASSWORD (contraseña PostgreSQL): " DB_PASSWORD
DB_PASSWORD="${DB_PASSWORD:-ChangeMe123!}"

read -p "EMAIL_HOST_USER (tu email Gmail): " EMAIL_HOST_USER
EMAIL_HOST_USER="${EMAIL_HOST_USER:-tu_email@gmail.com}"

read -sp "EMAIL_HOST_PASSWORD (app password de Google): " EMAIL_HOST_PASSWORD
EMAIL_HOST_PASSWORD="${EMAIL_HOST_PASSWORD:-}"
echo ""

echo ""
echo -e "${YELLOW}📌 PASO 5: Preparando despliegue en VPS${NC}"

ssh $VPS_USER@$VPS_IP << 'EOF'
    # Crear directorio de proyecto
    mkdir -p /home/dokploy/apps
    cd /home/dokploy/apps
    
    # Clonar repositorio si no existe
    if [ ! -d "FPCD" ]; then
        echo "Clonando repositorio..."
        git clone https://github.com/lcuper18/FPCD.git
    else
        echo "Repositorio ya existe, actualizando..."
        cd FPCD
        git pull origin main
        cd ..
    fi
    
    cd FPCD
    
    # Crear archivo .env desde .env.production
    cp .env.production .env
    
    echo "✓ Repositorio preparado en /home/dokploy/apps/FPCD"
EOF

echo -e "${GREEN}✓ Preparación completada${NC}"
echo ""

# Instrucciones finales
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  📝 PRÓXIMOS PASOS - COMPLETAR MANUALMENTE EN DOKPLOY          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "1. Abre en navegador: http://$DOKPLOY_IP:$DOKPLOY_PORT"
echo ""
echo "2. En el Dashboard, selecciona:"
echo "   • New Project"
echo "   • Nombre: $PROJECT_NAME"
echo "   • Descripción: Plataforma de devocionales cristianos"
echo ""
echo "3. Selecciona Docker Compose:"
echo "   • Source: Docker Compose"
echo "   • Root Directory: /home/dokploy/apps/FPCD"
echo "   • Docker Compose File: docker-compose.yml"
echo ""
echo "4. Configura Variables de Entorno:"
echo ""
echo "   DEBUG=False"
echo "   SECRET_KEY=$SECRET_KEY"
echo "   ALLOWED_HOSTS=fecadadia.com,www.fecadadia.com,148.230.92.233"
echo "   DB_NAME=fpcd_db"
echo "   DB_USER=admin_fpcd"
echo "   DB_PASSWORD=$DB_PASSWORD"
echo "   DB_HOST=db"
echo "   DB_PORT=5432"
echo "   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend"
echo "   EMAIL_HOST=smtp.gmail.com"
echo "   EMAIL_PORT=587"
echo "   EMAIL_USE_TLS=True"
echo "   EMAIL_HOST_USER=$EMAIL_HOST_USER"
echo "   EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD"
echo ""
echo "5. Dominio:"
echo "   • Domain: $DOMAIN"
echo "   • Dokploy configurará SSL automáticamente con Let's Encrypt"
echo ""
echo "6. Click en DEPLOY"
echo ""
echo -e "${GREEN}¡El despliegue debería completarse en ~5 minutos!${NC}"
echo ""
echo -e "${YELLOW}⏱️  Verificación post-despliegue:${NC}"
echo "   • https://$DOMAIN (debe cargar)"
echo "   • https://$DOMAIN/admin/ (panel admin)"
echo "   • Ver logs en Dokploy Dashboard"
echo ""
echo -e "${BLUE}📞 En caso de problemas:${NC}"
echo "   • Ver DESPLIEGUE_DOKPLOY.md para troubleshooting"
echo "   • Ver REPORTE_PRUEBAS.md para validación técnica"
echo ""
