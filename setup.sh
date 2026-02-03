#!/bin/bash

# Script de inicio rápido para Fe para Cada Día
# Este script configura el proyecto de forma automática

echo "==================================="
echo "Fe para Cada Día - Setup Script"
echo "==================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

echo "✅ Python $(python3 --version) encontrado"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Copiar archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones"
else
    echo "✅ Archivo .env ya existe"
fi

# Preguntar si quiere ejecutar migraciones
read -p "¿Deseas ejecutar las migraciones ahora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Ejecutando migraciones..."
    python manage.py makemigrations
    python manage.py migrate
    echo "✅ Migraciones completadas"
    
    # Preguntar si quiere crear superusuario
    read -p "¿Deseas crear un superusuario ahora? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python manage.py createsuperuser
    fi
fi

# Preguntar si quiere ejecutar el servidor
echo ""
echo "==================================="
echo "✅ Setup completado exitosamente!"
echo "==================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tus configuraciones"
echo "2. Asegúrate de tener PostgreSQL instalado y configurado"
echo "3. Ejecuta: source venv/bin/activate"
echo "4. Ejecuta: python manage.py runserver"
echo ""
read -p "¿Deseas iniciar el servidor de desarrollo ahora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Iniciando servidor..."
    python manage.py runserver
fi
