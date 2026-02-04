# Fe para Cada Día - Proyecto Django

## 🎯 Descripción del Proyecto

Aplicación web Django completa para el ministerio cristiano "Fe para Cada Día" con:
- ✅ Sistema de autenticación de usuarios
- ✅ Devocionales diarios con búsqueda por tema
- ✅ Newsletter con suscripciones
- ✅ Dashboard para colaboradores
- ✅ Materiales cristianos descargables
- ✅ Sistema de comentarios y favoritos
- ✅ PostgreSQL como base de datos
- ✅ Panel administrativo completo

---

## 🚀 Instalación Local

### 1. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones:
- SECRET_KEY
- DB_NAME, DB_USER, DB_PASSWORD (PostgreSQL)
- EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (para newsletter)

### 4. Crear base de datos PostgreSQL

```sql
CREATE DATABASE fe_para_cada_dia_db;
CREATE USER tu_usuario WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE fe_para_cada_dia_db TO tu_usuario;
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Correr el servidor de desarrollo

```bash
python manage.py runserver
```

Visita: `http://localhost:8000`

---

## 📦 Deployment en Hostinger

### Paso 1: Preparar el proyecto

1. **Instalar Git en Hostinger** (si no está instalado)
2. **Clonar o subir el proyecto** vía FTP/Git

### Paso 2: Configurar Python y entorno virtual

```bash
cd ~/public_html/fe_para_cada_dia
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Configurar PostgreSQL en Hostinger

1. Ve al panel de Hostinger → **Bases de Datos** → **PostgreSQL**
2. Crea una nueva base de datos
3. Anota: nombre, usuario, contraseña, host, puerto

### Paso 4: Configurar variables de entorno

Crea archivo `.env` en el servidor:

```bash
nano .env
```

Configura:
```
SECRET_KEY=tu-clave-super-segura-generada
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

DB_NAME=nombre_bd_postgres
DB_USER=usuario_postgres
DB_PASSWORD=password_postgres
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

### Paso 5: Colectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 6: Ejecutar migraciones

```bash
python manage.py migrate
```

### Paso 7: Crear superusuario

```bash
python manage.py createsuperuser
```

### Paso 8: Configurar Gunicorn

Crea archivo `gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
```

### Paso 9: Iniciar aplicación

```bash
gunicorn config.wsgi:application -c gunicorn_config.py
```

---

## 👥 Roles de Usuario

El sistema tiene 3 roles:

1. **Lector** (reader): Usuario estándar, puede leer y comentar
2. **Colaborador** (collaborator): Puede crear devocionales y materiales
3. **Administrador** (admin): Acceso completo al panel admin

Para cambiar roles, ve al admin de Django: `/admin/users/customuser/`

---

## 📝 Uso del Dashboard

### Para Colaboradores:

1. Inicia sesión
2. Ve a **Dashboard** en el menú
3. Accede al panel de administración
4. Crea devocionales, materiales, etc.

### Panel de Admin:

- `/admin/` → Panel administrativo completo
- Gestión de usuarios, devocionales, newsletter, materiales
- Moderación de comentarios
- Estadísticas de vistas y descargas

---

## 📊 Estructura del Proyecto

```
fe_para_cada_dia/
├── config/              # Configuración Django
├── users/               # App de usuarios
├── devotionals/         # App de devocionales
├── newsletter/          # App de newsletter
├── materials/           # App de materiales
├── templates/           # Templates HTML
├── static/              # CSS, JS, imágenes
├── media/               # Archivos subidos
├── requirements.txt     # Dependencias
├── manage.py            # Script de Django
└── .env                 # Variables de entorno
```

---

**Hecho con ❤️ para la gloria de Dios**

*"Toda la Escritura es inspirada por Dios y útil para enseñar" — 2 Timoteo 3:16*
