#!/bin/bash

# Script rápido para ejecutar el servidor de desarrollo
# Uso: ./run.sh

echo "🚀 Iniciando Fe para Cada Día..."

# Verificar que exista el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta: python3 -m venv venv"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor
echo "✅ Iniciando servidor en http://localhost:8000"
echo "📊 Admin disponible en http://localhost:8000/admin"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

python manage.py runserver
