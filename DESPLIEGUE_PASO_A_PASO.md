# 📋 GUÍA FINAL: DESPLEGAR EN DOKPLOY Y PROBAR

**Fecha**: 5 de Febrero de 2026  
**Status**: Proyecto listo, aguardando despliegue manual en Dokploy

---

## 🎯 Situación Actual

✅ **Proyecto completado 100%**
- Django app sin errores
- Docker funcional
- Todas las pruebas pasadas
- Código en GitHub
- Variables de entorno listas

❌ **Falta**: Desplegar manualmente en Dokploy

---

## 🚀 PASO 1: ACCEDER A DOKPLOY

1. Abre en tu navegador: **http://148.230.92.233:3000**
2. Inicia sesión con tus credenciales de Dokploy

---

## 🚀 PASO 2: CREAR NUEVO PROYECTO

En el Dashboard:
1. Haz clic en **"New Project"**
2. Nombre: `Fe para Cada Día`
3. Descripción: `Plataforma de devocionales cristianos`
4. Click en **Create**

---

## 🚀 PASO 3: CONFIGURAR GITHUB

1. En el proyecto recién creado, selecciona **"Connect Repository"**
2. Selecciona **GitHub** como fuente
3. Autoriza Dokploy con tu cuenta GitHub (si no lo has hecho)
4. Busca y selecciona: **lcuper18/FPCD**
5. Rama: **main**
6. Click en **Connect**

---

## 🚀 PASO 4: CONFIGURAR DOCKER COMPOSE

1. En **Deployment Settings**:
   - Source Type: **Docker Compose**
   - Root Directory: `/` (raíz)
   - Docker Compose File: `docker-compose.yml`

2. Click en **Next**

---

## 🚀 PASO 5: CONFIGURAR VARIABLES DE ENTORNO

Dokploy te pedirá las variables. Copia y personaliza estas:

```env
# ============ DJANGO ============
DEBUG=False
SECRET_KEY=django-insecure-tu-clave-secreta-aqui-minimo-50-caracteres
ALLOWED_HOSTS=fecadadia.com,www.fecadadia.com,148.230.92.233

# ============ DATABASE ============
DB_ENGINE=django.db.backends.postgresql
DB_NAME=fpcd_db
DB_USER=admin_fpcd
DB_PASSWORD=tu-contraseña-segura-aqui
DB_HOST=db
DB_PORT=5432

# ============ EMAIL (Gmail) ============
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_google

# ============ SITIO ============
SITE_NAME=Fe para Cada Día
ADMIN_EMAIL=admin@fecadadia.com
YOUTUBE_CHANNEL_URL=https://youtube.com/@TuCanal
```

⚠️ **Importante para Email de Gmail:**
1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Mail" y "Windows Computer"
3. Google generará una contraseña de 16 caracteres
4. Copia esa contraseña en `EMAIL_HOST_PASSWORD`

---

## 🚀 PASO 6: CONFIGURAR DOMINIO Y SSL

1. En **Domain Settings**:
   - Domain: `fecadadia.com`
   - Enable HTTPS: **✓ Sí**

2. Dokploy automáticamente:
   - Configurará Nginx como proxy reverso
   - Obtendrá certificado SSL con Let's Encrypt
   - Redirigirá HTTP → HTTPS

---

## 🚀 PASO 7: DESPLEGAR

1. Verifica toda la configuración
2. Click en **DEPLOY**
3. Dokploy automáticamente:
   - Clonará el repositorio
   - Construirá la imagen Docker
   - Ejecutará migraciones
   - Colectará static files
   - Iniciará los servicios
   - Configurará SSL

**⏱️ Tiempo aproximado: 5-10 minutos**

---

## 📊 MONITORIZAR DESPLIEGUE

En Dokploy Dashboard:

1. **Deployments Tab** → Ver estado en tiempo real
2. **Logs** → Ver output de construcción y ejecución
3. **Container Status** → Verificar que servicios estén healthy

---

## ✅ VERIFICAR DESPLIEGUE EXITOSO

Una vez completado, verifica:

### 1. Sitio Principal
```bash
curl -I https://fecadadia.com
# Debería devolver HTTP 200
```

### 2. Admin Panel
```bash
curl -I https://fecadadia.com/admin/
# Debería devolver HTTP 200 o 302 (redirección a login)
```

### 3. Static Files (CSS)
```bash
curl -I https://fecadadia.com/static/admin/css/base.css
# Debería devolver HTTP 200
```

### 4. En Navegador
- Abre: https://fecadadia.com
- Debería cargar la página de inicio
- Abre: https://fecadadia.com/admin/
- Debería mostrar formulario de login

---

## 🔐 CREDENCIALES INICIALES

**Panel Administrativo:**
- URL: `https://fecadadia.com/admin/`
- Usuario: `admin_prod`
- Contraseña: `TempPass123!`

⚠️ **ACCIÓN REQUERIDA INMEDIATAMENTE:**

Después de first login:
1. Ve a: Admin → Users → admin_prod
2. Cambia la contraseña a algo seguro y único
3. Guárdala en un lugar seguro

---

## 📋 CHECKLIST POST-DESPLIEGUE

- [ ] Sitio accesible en https://fecadadia.com
- [ ] Admin accesible en https://fecadadia.com/admin/
- [ ] SSL/TLS funcionando (navegador muestra cerrado seguro)
- [ ] Static files cargando correctamente
- [ ] Login al panel admin funciona
- [ ] Contraseña admin cambiada
- [ ] Base de datos funcionando
- [ ] Logs sin errores en Dokploy

---

## 🔧 TROUBLESHOOTING

### Error: "Connection refused"
- Verifica que Dokploy esté corriendo: `docker ps`
- Revisa logs en Dokploy dashboard

### Error: "502 Bad Gateway"
- Espera 1-2 minutos más, Django está inicializando
- Verifica logs en Dokploy

### Error: "SSL certificate not yet valid"
- Dokploy tarda 2-5 minutos en obtener certificado
- Espera y recarga

### Admin no funciona
- Verifica variables de entorno en Dokploy
- Revisa logs del contenedor web

---

## 📞 DOCUMENTACIÓN ADICIONAL

- [LISTO_PRODUCCION.md](./LISTO_PRODUCCION.md) - Resumen final
- [REPORTE_PRUEBAS.md](./REPORTE_PRUEBAS.md) - Validación técnica
- [DESPLIEGUE_DOKPLOY.md](./docs/guides/DESPLIEGUE_DOKPLOY.md) - Documentación completa

---

## 🎊 DESPUÉS DEL DESPLIEGUE

Una vez desplegado exitosamente:

1. **Crear contenido:**
   - Accede a `/admin/`
   - Crea categorías de devocionales
   - Sube devocionales
   - Configura newsletter

2. **Configurar Email:**
   - Prueba enviando email desde admin
   - Verifica que llega correctamente

3. **Monitoring:**
   - Revisa logs regularmente
   - Monitoriza uso de recursos
   - Configura backups automáticos

---

## 📈 PRÓXIMOS PASOS (DESPUÉS DE ESTAR LIVE)

1. **DNS:** Verifica que fecadadia.com apunta a 148.230.92.233
2. **Backups:** Configura backups automáticos en Dokploy
3. **Monitoring:** Configura alertas en Dokploy
4. **Analytics:** Integra Google Analytics si es necesario
5. **SEO:** Configura sitemap.xml y robots.txt
6. **Email:** Configura SPF/DKIM para mejor entrega

---

**¡Listo para desplegar! 🚀**

Si necesitas ayuda, revisa la documentación o contacta al equipo de desarrollo.
