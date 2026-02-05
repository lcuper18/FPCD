# 🚀 Guía de Despliegue en Dokploy

## 📋 Pasos para desplegar en tu VPS con Dokploy

### 1. Acceder a Dokploy

Abre en tu navegador: `http://148.230.92.233:3000` (o tu IP de VPS)

### 2. Crear nuevo proyecto

1. Dashboard → **New Project**
2. Nombre: `Fe para Cada Día`
3. Descripción: `Plataforma de devocionales cristianos`

### 3. Conectar GitHub

1. Selecciona **GitHub Repository**
2. Autoriza Dokploy con tu cuenta GitHub
3. Selecciona: `lcuper18/FPCD`
4. Rama: `main`
5. Base directory: `/` (raíz)

### 4. Configurar Docker Compose

1. **Source Type**: Docker Compose
2. **Docker Compose File**: `docker-compose.yml`
3. **Root Directory**: `/`

### 5. Configurar Variables de Entorno

Dokploy pedirá las variables. Cópialas desde `.env.production`:

```env
DEBUG=False
SECRET_KEY=django-insecure-CAMBIAR-ESTO-50-CARACTERES
ALLOWED_HOSTS=fecadadia.com,www.fecadadia.com,148.230.92.233
DB_NAME=fpcd_db
DB_USER=admin_fpcd
DB_PASSWORD=tu-contraseña-segura
DB_HOST=db
DB_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_google
```

⚠️ **Para Google Gmail:**
1. Ir a: https://myaccount.google.com/apppasswords
2. Generar "App Password"
3. Copiar en `EMAIL_HOST_PASSWORD`

### 6. Configurar Dominio

1. En Dokploy → Project Settings
2. **Domain**: `fecadadia.com`
3. Dokploy automáticamente:
   - Configura Nginx proxy
   - Obtiene SSL con Let's Encrypt
   - Redirige HTTP → HTTPS

### 7. Desplegar

Haz clic en **Deploy** y Dokploy:
- ✅ Clona el repo desde GitHub
- ✅ Construye imagen Docker
- ✅ Ejecuta migraciones
- ✅ Collect static files
- ✅ Inicia servicios
- ✅ Configura SSL

---

## ✅ Verificación Post-Despliegue

### 1. Verificar sitio

```bash
# En tu navegador
https://fecadadia.com  # debe cargar la página
https://fecadadia.com/admin/  # acceso a admin
```

### 2. Ver logs

En Dokploy → Deployments → Logs

```
[2026-02-05 12:00:00 +0000] [15] [INFO] Starting gunicorn
[2026-02-05 12:00:01 +0000] [16] [INFO] Booting worker with pid: 16
```

### 3. Verificar base de datos

```bash
# SSH a VPS
ssh root@148.230.92.233

# Conectar a PostgreSQL
docker exec fpcd_db psql -U admin_fpcd -d fpcd_db -c "SELECT * FROM django_migrations LIMIT 5;"
```

### 4. Verificar archivos estáticos

```bash
# Deben cargar en:
https://fecadadia.com/static/admin/css/base.css
```

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'src'"

**Solución**: Verificar que el `docker-compose.yml` usa el contexto correcto
```yaml
build:
  context: .
  dockerfile: docker/Dockerfile
```

### Error: "psycopg2 connection refused"

**Solución**: Verificar que `DB_HOST=db` (nombre del servicio, no IP)

### SSL no funciona

**Solución**: Dokploy tarda ~5 min en obtener certificado. Esperar y verificar logs.

### Base de datos vacía

**Solución**: Ejecutar en Dokploy console:
```bash
docker-compose exec web python manage.py seed_data
```

---

## 📞 Soporte

- Documentación completa: [docs/guides/DOKPLOY.md](../guides/DOKPLOY.md)
- GitHub: https://github.com/lcuper18/FPCD
- Email: admin@fecadadia.com
