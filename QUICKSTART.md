# 🚀 Guía de Inicio Rápido - Fe para Cada Día

## ⚡ Instalación en 5 Minutos

### Paso 1: Descargar el Proyecto
```bash
cd /home/dw/workspace/fe_para_cada_dia
```

### Paso 2: Ejecutar Script de Instalación
```bash
./setup.sh
```

El script hará automáticamente:
- ✅ Crear entorno virtual
- ✅ Instalar dependencias
- ✅ Crear archivo .env
- ✅ Ejecutar migraciones (opcional)
- ✅ Crear superusuario (opcional)
- ✅ Iniciar servidor (opcional)

### Paso 3: Configurar Variables de Entorno

Edita el archivo `.env`:

```bash
nano .env
```

**Configuración mínima para desarrollo local:**

```env
SECRET_KEY=django-insecure-dev-key-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (crea la BD primero)
DB_NAME=fe_para_cada_dia_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### Paso 4: Crear Base de Datos PostgreSQL

```bash
# Conéctate a PostgreSQL
sudo -u postgres psql

# Dentro de PostgreSQL:
CREATE DATABASE fe_para_cada_dia_db;
CREATE USER tu_usuario WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE fe_para_cada_dia_db TO tu_usuario;
\q
```

### Paso 5: Iniciar el Proyecto

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

---

## 🌐 Acceder a la Aplicación

| Página | URL | Descripción |
|--------|-----|-------------|
| **Home** | http://localhost:8000/ | Página principal con devocional del día |
| **Admin** | http://localhost:8000/admin/ | Panel administrativo Django |
| **Devocionales** | http://localhost:8000/devocionales/ | Lista de todos los devocionales |
| **Materiales** | http://localhost:8000/materiales/ | Biblioteca de recursos |
| **Registro** | http://localhost:8000/usuarios/registro/ | Crear nueva cuenta |
| **Login** | http://localhost:8000/usuarios/login/ | Iniciar sesión |
| **Newsletter** | http://localhost:8000/newsletter/suscribirse/ | Suscripción al newsletter |
| **Dashboard** | http://localhost:8000/usuarios/dashboard/ | Panel de colaboradores |

---

## 👤 Primeros Pasos Después de Instalar

### 1. Acceder al Admin

1. Ve a: http://localhost:8000/admin/
2. Ingresa con tu superusuario
3. Explora las secciones disponibles

### 2. Crear Categorías

1. Admin → **Categorías** → **Agregar categoría**
2. Crea algunas categorías:
   - 📖 Esperanza
   - 🙏 Oración
   - ❤️ Amor de Dios
   - ✝️ Fe
   - 🌟 Salvación

### 3. Crear tu Primer Devocional

1. Admin → **Devocionales** → **Agregar devocional**
2. Completa los campos:
   - **Título**: "Dios Nunca Te Abandona"
   - **Versículo**: "Nunca te dejaré; jamás te abandonaré"
   - **Referencia**: Hebreos 13:5
   - **Contenido**: Escribe tu devocional
   - **Fecha de publicación**: Hoy
   - **Estado**: Publicado
3. Guarda

### 4. Crear Usuarios de Prueba

1. Admin → **Usuarios** → **Agregar usuario**
2. Crea usuarios con diferentes roles:
   - **Lector**: Usuario normal
   - **Colaborador**: Puede crear contenido
   - **Admin**: Acceso completo

---

## 🎨 Personalizar el Sitio

### Cambiar Nombre del Sitio

Edita `.env`:
```env
SITE_NAME=Mi Ministerio Cristiano
```

### Agregar Canal de YouTube

Edita `.env`:
```env
YOUTUBE_CHANNEL_URL=https://youtube.com/@TuCanal
```

### Cambiar Colores

Edita `static/css/main.css`:
```css
:root {
    --primary-color: #TU_COLOR;
}
```

---

## 📧 Configurar Email (Gmail)

### 1. Habilitar Autenticación de 2 Factores

1. Ve a tu cuenta de Google
2. Seguridad → Verificación en 2 pasos
3. Actívala

### 2. Generar Contraseña de Aplicación

1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Correo" y "Otro"
3. Copia la contraseña generada

### 3. Configurar en .env

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=la_password_generada
```

---

## 🎯 Casos de Uso Comunes

### Como Administrador

1. **Crear devocional diario**:
   - Admin → Devocionales → Agregar
   - Establecer fecha = hoy
   - Publicar

2. **Moderar comentarios**:
   - Admin → Comentarios
   - Marcar como aprobado

3. **Gestionar suscriptores**:
   - Admin → Newsletter → Suscriptores
   - Ver lista completa

### Como Colaborador

1. **Acceder al dashboard**:
   - Login → Dashboard
   - Click en "Crear Devocional"

2. **Subir materiales**:
   - Dashboard → Gestionar Materiales
   - Agregar nuevo material

### Como Usuario

1. **Leer devocional del día**:
   - Ir a home
   - Leer contenido completo

2. **Agregar a favoritos**:
   - Click en ❤️ Favoritos
   - Ver "Mis Favoritos"

3. **Comentar**:
   - Leer devocional
   - Escribir comentario (espera aprobación)

---

## 🐛 Solución de Problemas

### Error: "No module named 'django'"

```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "FATAL: database does not exist"

```bash
# Crea la base de datos PostgreSQL primero
sudo -u postgres psql
CREATE DATABASE fe_para_cada_dia_db;
```

### Error: "SECRET_KEY required"

```bash
# Asegúrate de tener el archivo .env
cp .env.example .env
# Edita .env con tus configuraciones
```

### Los estilos CSS no se ven

```bash
# Colecta archivos estáticos
python manage.py collectstatic
```

---

## 📊 Comandos Útiles de Django

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Colectar archivos estáticos
python manage.py collectstatic

# Iniciar servidor de desarrollo
python manage.py runserver

# Abrir shell de Django
python manage.py shell

# Ver todas las URLs disponibles
python manage.py show_urls  # requiere django-extensions
```

---

## 🔒 Cambiar Rol de Usuario

### Método 1: Desde el Admin

1. Admin → Usuarios → Seleccionar usuario
2. Cambiar campo "Rol"
3. Guardar

### Método 2: Desde la Shell de Django

```bash
python manage.py shell
```

```python
from users.models import CustomUser

# Cambiar a colaborador
user = CustomUser.objects.get(email='usuario@ejemplo.com')
user.role = 'collaborator'
user.save()
```

---

## 📝 Próximos Pasos

1. ✅ **Crear contenido inicial**: 5-10 devocionales
2. ✅ **Configurar newsletter**: Email settings
3. ✅ **Personalizar diseño**: Logo, colores
4. ✅ **Invitar colaboradores**: Crear cuentas
5. ✅ **Testear funcionalidades**: Comentarios, favoritos
6. ✅ **Preparar deployment**: Leer DEPLOYMENT.md

---

## 🎉 ¡Listo!

Tu proyecto **Fe para Cada Día** está funcionando. Ahora puedes:

- 📖 Crear devocionales diarios
- 👥 Gestionar usuarios
- 💌 Enviar newsletters
- 📚 Compartir materiales cristianos
- 🎨 Personalizar según tu ministerio

---

**¿Necesitas ayuda?** Revisa README.md para documentación completa o DEPLOYMENT.md para publicar en producción.

**Bendiciones en tu ministerio digital! 🙏**
