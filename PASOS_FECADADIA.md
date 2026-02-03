# 🚀 Próximos Pasos - fecadadia.com

Tu dominio **fecadadia.com** está comprado y listo. Sigue estos pasos **en orden** para tenerlo en línea:

## ⏱️ Tiempo estimado: 30-60 minutos

## 📋 PASO 1: Obtener IP de tu VPS (5 minutos)

```bash
# Conecta por SSH a tu VPS Hostinger:
ssh root@tu-ip-vps

# Una vez conectado, ejecuta:
hostname -I

# Anota la dirección IP (ej: 148.230.92.233)
```

## 📍 PASO 2: Configurar DNS en Hostinger (5 minutos)

1. Accede a **hPanel** → https://hpanel.hostinger.com
2. Selecciona **fecadadia.com**
3. Ve a **DNS / Nameservers**
4. Selecciona **DNS Records / Registros DNS**
5. Modifica el registro **A**:

| Campo | Valor |
|-------|-------|
| Type | A |
| Name | @ |
| Value | **TU-IP-VPS** |
| TTL | 3600 |

6. Agrega otro registro **A** para www:

| Campo | Valor |
|-------|-------|
| Type | A |
| Name | www |
| Value | **TU-IP-VPS** |
| TTL | 3600 |

📌 **Reemplaza TU-IP-VPS con tu dirección IP obtenida en PASO 1**

## ⏳ PASO 3: Esperar propagación DNS (15-30 minutos)

```bash
# En tu terminal local, verifica:
nslookup fecadadia.com

# Cuando veas tu IP en la respuesta, DNS está listo
# Ejemplo de respuesta correcta:
# Server: 8.8.8.8
# Address: 8.8.8.8#53
# Non-authoritative answer:
# Name: fecadadia.com
# Address: 148.230.92.233 ✅
```

**O usa**: https://www.whatsmydns.net/?d=fecadadia.com

## 🐳 PASO 4: Desplegar con Dokploy (10 minutos)

### En tu navegador:

1. Abre Dokploy en tu VPS (pregunta a soporte Hostinger si no sabes la URL)
2. Nuevo **Project** → **GitHub Repository**
3. Autoriza GitHub
4. Selecciona: **lcuper18/FPCD**
5. Rama: **main**
6. **Deployment Type**: Docker Compose
7. **Docker Compose File**: `docker-compose.yml`

### Variables de entorno en Dokploy:

Usa el archivo [.env.fecadadia](.env.fecadadia) como referencia o copia:

```env
DEBUG=False
SECRET_KEY=django-insecure-GENERA-UNA-CLAVE-ALEATORIA
ALLOWED_HOSTS=fecadadia.com,www.fecadadia.com,localhost
DB_NAME=fpcd_db
DB_USER=admin_fpcd
DB_PASSWORD=tu-contraseña-fuerte
DB_HOST=db
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-google
```

8. Haz clic en **Deploy**

### Dokploy automáticamente:
- ✅ Clona el repositorio
- ✅ Construye la imagen Docker
- ✅ Crea base de datos PostgreSQL
- ✅ Ejecuta migraciones
- ✅ Obtiene certificado SSL (Let's Encrypt)
- ✅ Configura Nginx
- ✅ Inicia servicios

⏱️ **Espera 5-10 minutos** a que termine

## ✅ PASO 5: Verificar que todo funciona (5 minutos)

```bash
# En tu terminal:

# 1. Verificar DNS
nslookup fecadadia.com
# Debe mostrar tu IP

# 2. Verificar que responde
curl -I https://fecadadia.com
# Debe mostrar HTTP/2 200

# 3. Verificar certificado SSL
curl -I https://fecadadia.com/admin
# Debe mostrar certificado válido
```

### En tu navegador:

1. Abre https://fecadadia.com
2. Deberías ver tu sitio
3. Accede a https://fecadadia.com/admin
4. Inicia sesión con superusuario

## 🎯 URLs finales

| Recurso | URL |
|---------|-----|
| **Página principal** | https://fecadadia.com |
| **Admin** | https://fecadadia.com/admin |
| **Devocionales** | https://fecadadia.com/devocionales/ |
| **Newsletter** | https://fecadadia.com/newsletter/suscribirse/ |

## 🆘 Si algo no funciona

1. **"Connection refused"**: DNS aún no propagó, espera más
2. **"502 Bad Gateway"**: Django está iniciando, espera 2-3 min
3. **"Certificate error"**: SSL está generándose, espera 5 min
4. **"Page not found"**: Verifica ALLOWED_HOSTS en .env

### Ver logs:

```bash
# Conecta al VPS
ssh root@tu-ip-vps

# Ver logs de Docker
docker-compose logs -f web
docker-compose logs -f db
```

## 📚 Documentación completa

- [DOMINIO_FECADADIA.md](DOMINIO_FECADADIA.md) - Guía completa de DNS
- [DOKPLOY.md](DOKPLOY.md) - Despliegue detallado
- [.env.fecadadia](.env.fecadadia) - Variables de entorno ejemplo

## 🎊 Una vez en línea

1. Crea superusuario:
```bash
docker-compose exec web python manage.py createsuperuser
```

2. Accede a admin y crea:
   - Categorías de devocionales
   - Devocionales iniciales
   - Materiales

3. Personaliza:
   - Logo en templates/base.html
   - Colores en static/css/main.css
   - Información de contacto

## 📞 Soporte

- Hostinger: support.hostinger.com
- Dokploy: https://dokploy.com/docs
- Este proyecto: https://github.com/lcuper18/FPCD

---

**¡Estás a menos de 1 hora de tener tu sitio en línea!** 🚀

Próximas dudas? Pregunta en los comentarios de GitHub.

*"Confía en que el Señor completará la buena obra que ha comenzado en ti" — Filipenses 1:6*
