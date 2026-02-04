# 🐳 Despliegue con Dokploy (Hostinger)

Dokploy simplifica significativamente el despliegue de aplicaciones Docker. Esta guía te muestra cómo desplegar **Fe para Cada Día** en tu VPS de Hostinger usando Dokploy.

## 📋 Prerequisitos

- ✅ VPS en Hostinger con Dokploy instalado
- ✅ Repositorio GitHub: https://github.com/lcuper18/FPCD
- ✅ Variables de entorno configuradas

## 🚀 Opción 1: Despliegue desde GitHub (Recomendado)

### Paso 1: Acceder a Dokploy

1. Abre la interfaz web de Dokploy en tu VPS
2. Navega a **Projects** → **New Project**

### Paso 2: Conectar GitHub

1. Selecciona **GitHub Repository** como fuente de despliegue
2. Autoriza Dokploy con tu cuenta de GitHub
3. Selecciona el repositorio **lcuper18/FPCD**
4. Selecciona rama: **main**

### Paso 3: Configurar despliegue

1. **Deployment Type**: Selecciona **Docker Compose**
2. **Base Directory**: Dejar vacío o `/` (raíz del repositorio)
3. **Docker Compose File**: `docker-compose.yml`

### Paso 4: Configurar variables de entorno

Dokploy te pedirá las variables de entorno. Aquí está la configuración:

```env
# Django
DEBUG=False
SECRET_KEY=django-insecure-tu-clave-secreta-50-caracteres
ALLOWED_HOSTS=fecadadia.com,www.fecadadia.com,ip-vps.com

# Base de Datos PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=fpcd_db
DB_USER=admin_fpcd
DB_PASSWORD=tu-contraseña-segura-aqui
DB_HOST=db
DB_PORT=5432

# Email (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-google
```

⚠️ **Importante**: Para Gmail, debes:
1. Ir a https://myaccount.google.com/apppasswords
2. Generar una "App Password" (no es tu contraseña normal)
3. Usar esa contraseña en `EMAIL_HOST_PASSWORD`

### Paso 5: Desplegar

1. Haz clic en **Deploy**
2. Dokploy automáticamente:
   - Clonará el repositorio
   - Construirá la imagen Docker
   - Ejecutará las migraciones
   - Iniciará los servicios
   - Configurará Nginx como proxy inverso
   - Configurará SSL (Let's Encrypt)

## 🐳 Opción 2: Despliegue desde Docker Compose

Si prefieres tener más control, puedes subir manualmente:

### Paso 1: Conectar VPS por SSH

```bash
ssh root@tu-ip-vps
cd /home/dokploy/apps
```

### Paso 2: Clonar repositorio

```bash
git clone https://github.com/lcuper18/FPCD.git
cd FPCD
```

### Paso 3: Crear archivo .env

```bash
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=django-insecure-tu-clave-secreta
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_NAME=fpcd_db
DB_USER=admin_fpcd
DB_PASSWORD=tu-contraseña
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
EOF
```

### Paso 4: Desplegar con Docker Compose

```bash
docker-compose -f docker-compose.yml up -d
```

## 🔧 Variables de entorno detalladas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DEBUG` | Modo desarrollo (siempre False en prod) | `False` |
| `SECRET_KEY` | Clave secreta Django (genera una nueva) | `django-insecure-...` |
| `ALLOWED_HOSTS` | Dominios permitidos separados por comas | `ejemplo.com,www.ejemplo.com` |
| `DB_NAME` | Nombre de base de datos PostgreSQL | `fpcd_db` |
| `DB_USER` | Usuario PostgreSQL | `admin_fpcd` |
| `DB_PASSWORD` | Contraseña PostgreSQL | `mi-contraseña-segura` |
| `DB_HOST` | Host de base de datos | `db` (si está en mismo compose) |
| `DB_PORT` | Puerto PostgreSQL | `5432` |
| `EMAIL_HOST_USER` | Email para enviar newsletters | `tu-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Contraseña aplicación Gmail | `xxxx xxxx xxxx xxxx` |

## 📱 Acceder a la aplicación

Una vez desplegada:

```
🌐 Frontend: https://fecadadia.com
🔐 Admin: https://fecadadia.com/admin
```

## 🛠️ Operaciones útiles en Dokploy

### Ver logs

```bash
# En Dokploy UI: Dashboard → Ver logs
# O por SSH:
docker-compose logs -f web
```

### Crear superusuario

```bash
docker-compose exec web python manage.py createsuperuser
```

### Hacer migraciones

```bash
docker-compose exec web python manage.py migrate
```

### Recolectar archivos estáticos

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Reiniciar servicios

```bash
docker-compose restart
```

## 🔄 Redesplegues automáticos

### Opción 1: GitHub Webhooks (Automático)

Dokploy configura webhooks de GitHub automáticamente. Cada `push` a `main`:
1. GitHub notifica a Dokploy
2. Dokploy clona cambios
3. Reconstruye imagen Docker
4. Redeploya automáticamente

### Opción 2: Manual

```bash
cd FPCD
git pull origin main
docker-compose up -d --build
```

## 🔒 Configuración de seguridad

### Generar SECRET_KEY fuerte

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Configurar SSL en Dokploy

Dokploy automáticamente:
- ✅ Configura Nginx
- ✅ Obtiene certificado Let's Encrypt
- ✅ Redirige HTTP → HTTPS
- ✅ Renueva automáticamente

### Base de datos segura

- ✅ PostgreSQL en contenedor aislado
- ✅ Datos persistentes en volumen
- ✅ Conexión interna (no expuesta)
- ✅ Contraseña fuerte obligatoria

## 📊 Monitoreo en Dokploy

La interfaz de Dokploy te muestra:
- 📈 CPU y memoria
- 📊 Tráfico de red
- 📝 Logs en tiempo real
- ⚡ Estado de servicios
- 🔄 Histórico de despliegues

## 🆘 Solución de problemas

### "Migraciones fallidas"

```bash
docker-compose exec web python manage.py migrate --no-input
```

### "Archivo estático no aparece"

```bash
docker-compose exec web python manage.py collectstatic --noinput --clear
```

### "Error de conexión a base de datos"

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs de DB
docker-compose logs db
```

### "Puerto 8000 en uso"

En `docker-compose.yml`, cambiar:
```yaml
ports:
  - "8001:8000"  # Usar 8001 en lugar de 8000
```

### "Permisos de archivos"

```bash
docker-compose exec web chown -R django:django /app
```

## ✅ Checklist de despliegue

- [ ] Repositorio GitHub actualizado
- [ ] Variables `.env` configuradas
- [ ] Contraseña PostgreSQL fuerte
- [ ] Email Gmail con App Password
- [ ] SECRET_KEY generada
- [ ] ALLOWED_HOSTS configurado
- [ ] Dokploy conectado a GitHub
- [ ] Despliegue completado
- [ ] HTTPS funcionando
- [ ] Admin accesible
- [ ] Newsletter funcionando
- [ ] Backups configurados

## 🎯 Próximos pasos

1. **Acceder a admin**: https://tu-dominio.com/admin
2. **Crear superusuario** (si no lo hizo automáticamente)
3. **Agregar categorías** de devocionales
4. **Crear devocionales** de ejemplo
5. **Personalizar** templates y colores
6. **Configurar email** para newsletter
7. **Invitar colaboradores** a la plataforma

## 📚 Documentación adicional

- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Clonar desde GitHub
- [DEPLOYMENT.md](DEPLOYMENT.md) - Despliegue manual (alternativa)
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida
- [README.md](README.md) - Documentación técnica

---

**Dokploy Documentation**: https://dokploy.com  
**Fe para Cada Día Repository**: https://github.com/lcuper18/FPCD  
**Última actualización**: 3 de Febrero de 2026
