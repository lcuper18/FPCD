# 🌐 Configuración de Dominio - fecadadia.com

Tu dominio **fecadadia.com** está listo para conectarse a tu VPS de Hostinger. Aquí está la guía paso a paso.

## 📋 Información que necesitas

Antes de empezar, obtén esta información de tu VPS en Hostinger:

```bash
# Conecta por SSH a tu VPS y ejecuta:
hostname -I
```

Esto te dará la **dirección IP de tu VPS** (ej: 148.230.92.233)

## 🔧 Paso 1: Configurar DNS en Hostinger

### En el panel de Hostinger (hPanel):

1. Accede a **hPanel** → https://hpanel.hostinger.com
2. Selecciona **fecadadia.com** en tus dominios
3. Ve a **DNS / Nameservers**
4. Selecciona **Custom DNS / Nameservers personalizados**
5. Reemplaza los nameservers con los de tu VPS (o deja los predeterminados si el VPS está en Hostinger)

### Opción A: Si el VPS está en Hostinger

Los nameservers deben ser:
```
ns1.hostinger.com
ns2.hostinger.com
ns3.hostinger.com
```

### Opción B: DNS personalizado (más recomendado)

1. Ve a **DNS Records / Registros DNS**
2. Busca el campo **A Record** (IPv4)
3. Agrega:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | TU-IP-VPS | 3600 |
| A | www | TU-IP-VPS | 3600 |
| CNAME | www | fecadadia.com | 3600 |

**Reemplaza `TU-IP-VPS`** con la dirección IP de tu VPS (ej: 148.230.92.233)

## ⏳ Esperando propagación DNS

Los cambios de DNS tardan entre **5 minutos a 48 horas** en propagarse globalmente.

Para verificar si DNS ya está configurado:

```bash
# En tu terminal local
nslookup fecadadia.com
dig fecadadia.com

# Deberías ver tu IP de VPS
```

O usa: https://www.whatsmydns.net/?d=fecadadia.com

## 🚀 Paso 2: Configurar Dokploy con tu dominio

Una vez que DNS esté propagado, configura Dokploy:

### En Dokploy Dashboard:

1. Crea un nuevo **Proyecto** o edita uno existente
2. Ve a **Settings / Configuración**
3. En **Domains / Dominios** agrega:
   - `fecadadia.com`
   - `www.fecadadia.com`

### Configurar en docker-compose.yml

Dokploy automáticamente configura Nginx. Si necesitas hacerlo manualmente:

```yaml
services:
  web:
    environment:
      ALLOWED_HOSTS: fecadadia.com,www.fecadadia.com,localhost
```

## 🔒 Paso 3: SSL/TLS (HTTPS)

### Automático con Dokploy

Dokploy automáticamente obtiene certificado Let's Encrypt para:
- `fecadadia.com`
- `www.fecadadia.com`

**No necesitas hacer nada**, Dokploy maneja todo.

### Verificar certificado

```bash
# En tu terminal
curl -I https://fecadadia.com

# Deberías ver: HTTP/2 200
```

## 📱 Paso 4: Redirecciones

### Redirigir www a sin www (Recomendado)

En Dokploy o Nginx:
```nginx
server {
    listen 80;
    server_name www.fecadadia.com;
    return 301 https://fecadadia.com$request_uri;
}
```

O en Hostinger cPanel (si usas cPanel):
- Settings → Redirect → www.fecadadia.com → https://fecadadia.com

## 🧪 Verificación

Después de configurar:

```bash
# 1. Verificar DNS
nslookup fecadadia.com
# Debe mostrar tu IP de VPS

# 2. Verificar conexión HTTP
curl -I http://fecadadia.com
# Debe redirigir a HTTPS (301)

# 3. Verificar HTTPS
curl -I https://fecadadia.com
# Debe mostrar 200 y el certificado válido

# 4. Verificar certificado
openssl s_client -connect fecadadia.com:443
# Debe mostrar certificado válido de Let's Encrypt
```

## ✅ Checklist de configuración

- [ ] IP del VPS obtenida
- [ ] Registros A/CNAME configurados en Hostinger
- [ ] DNS propagado (verificar con nslookup)
- [ ] ALLOWED_HOSTS actualizado en Django
- [ ] Dokploy configurado con dominio
- [ ] SSL activo en Dokploy
- [ ] https://fecadadia.com accesible
- [ ] https://www.fecadadia.com funciona
- [ ] Admin en https://fecadadia.com/admin accesible
- [ ] Email configurado (opcional)

## 🚨 Problemas comunes

### "Connection refused" o "ERR_CONNECTION_REFUSED"

**Causa**: Probablemente DNS aún no está propagado
**Solución**: 
```bash
# Espera 15-30 minutos
# Borra caché DNS en tu navegador (Ctrl+Shift+Delete)
# O accede directamente por IP: http://TU-IP-VPS
```

### "Certificate problem" o "untrusted certificate"

**Causa**: Certificado Let's Encrypt aún se está generando
**Solución**:
```bash
# En tu VPS:
docker-compose logs web
# Busca: "Successfully received certificate"
```

### "502 Bad Gateway"

**Causa**: Django no está respondiendo
**Solución**:
```bash
# Verifica que Django está corriendo:
docker-compose ps

# Ver logs:
docker-compose logs web
```

### "Timeout o muy lento"

**Causa**: Puede ser tráfico de la propagación DNS
**Solución**: 
- Espera 1-2 horas
- Verifica que Dokploy tiene suficientes recursos

## 📧 Configuración de Email (Recomendado)

Para enviar newsletters desde **fecadadia.com**:

### Usar Gmail:

1. Ve a https://myaccount.google.com/apppasswords
2. Genera App Password (no es tu contraseña normal)
3. En Dokploy, configura:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx
DEFAULT_FROM_EMAIL=noreply@fecadadia.com
```

### O usar Hostinger Email:

Si compras email en Hostinger:

```env
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=info@fecadadia.com
EMAIL_HOST_PASSWORD=tu-contraseña-email
DEFAULT_FROM_EMAIL=info@fecadadia.com
```

## 🎯 URLs finales

Una vez todo configurado:

| Recurso | URL |
|---------|-----|
| **Página principal** | https://fecadadia.com |
| **Admin** | https://fecadadia.com/admin |
| **Newsletter** | https://fecadadia.com/newsletter/suscribirse/ |
| **Devocionales** | https://fecadadia.com/devocionales/ |
| **Materiales** | https://fecadadia.com/materiales/ |

## 📞 Soporte Hostinger

Si necesitas ayuda:
- 📧 Soporte: support.hostinger.com
- 💬 Live chat en hPanel
- 📞 Teléfono: +1-844-551-9509

## 🔐 Recomendaciones de seguridad

1. **Firewall**: Abre puertos 80 (HTTP) y 443 (HTTPS)
2. **Backups**: Configura backups automáticos en Dokploy
3. **Contraseñas**: Cambia todas las contraseñas por defecto
4. **Admin**: Crea superusuario con contraseña fuerte
5. **Email**: Usa App Passwords, no contraseñas normales
6. **Logs**: Revisa logs regularmente en Dokploy

## 📚 Documentación relacionada

- [DOKPLOY.md](DOKPLOY.md) - Despliegue con Dokploy
- [README.md](README.md) - Documentación técnica
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Desarrollo local

---

**Dominio**: fecadadia.com  
**VPS**: Hostinger  
**Administrador**: Dokploy  
**Última actualización**: 3 de Febrero de 2026

*"Confía en el Señor con todo tu corazón" — Proverbios 3:5*
