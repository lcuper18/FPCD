# Usar imagen oficial de Python
FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código de la aplicación (todo)
COPY . .

# Verificar estructura (debug)
RUN ls -la /app/ && ls -la /app/config/ || true

# Crear usuario no-root
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

# Recolectar archivos estáticos (comando opcional para producción)
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
