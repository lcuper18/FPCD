# 🚀 Configuración rápida desde GitHub

## Clonar el repositorio

```bash
git clone https://github.com/lcuper18/FPCD.git
cd FPCD
```

## Instalación automática (Opción 1 - Recomendado)

```bash
chmod +x setup.sh
./setup.sh
```

Esto instalará automáticamente:
- ✅ Entorno virtual
- ✅ Dependencias
- ✅ Base de datos (SQLite para desarrollo)
- ✅ Migraciones

## Instalación manual (Opción 2)

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## Ejecutar servidor

```bash
chmod +x run.sh
./run.sh
```

O manualmente:
```bash
source venv/bin/activate
python manage.py runserver
```

## Acceder a la aplicación

- **Frontend**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## Configuración para Hostinger

1. **Crear archivo .env** con variables de producción:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nombre_db
DB_USER=usuario_db
DB_PASSWORD=contraseña
DB_HOST=servidor.db.com
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

2. **Seguir DEPLOYMENT.md**:
   - Configurar PostgreSQL
   - Instalar Gunicorn
   - Configurar Nginx
   - Configurar SSL

## Estructura del repositorio

```
FPCD/
├── config/              # Configuración Django
├── users/               # App de usuarios
├── devotionals/         # App de devocionales
├── newsletter/          # App de newsletter
├── materials/           # App de materiales
├── templates/           # Templates HTML
├── static/              # CSS, JS, imágenes
├── manage.py            # CLI de Django
├── requirements.txt     # Dependencias
├── setup.sh            # Script de instalación
├── run.sh              # Script para ejecutar
├── .env.example        # Plantilla de configuración
├── README.md           # Documentación técnica
├── DEPLOYMENT.md       # Guía de despliegue
├── QUICKSTART.md       # Inicio rápido
└── CHECKLIST.md        # Verificación
```

## Solución de problemas

### "ModuleNotFoundError: No module named 'django'"

```bash
# Asegúrate de activar el venv
source venv/bin/activate

# O instala directamente
pip install django==5.0.2
```

### "psycopg2 error"

Para PostgreSQL, instala:
```bash
pip install psycopg2-binary
```

### "Port 8000 already in use"

```bash
# Usar otro puerto
python manage.py runserver 0.0.0.0:8001
```

### Migraciones fallidas

```bash
python manage.py migrate --fake-initial
```

## Próximos pasos

1. ✅ Crear superusuario
2. ✅ Acceder a http://localhost:8000/admin
3. ✅ Crear categorías de devocionales
4. ✅ Agregar devocionales
5. ✅ Personalizar templates y CSS
6. ✅ Configurar email para newsletter
7. ✅ Desplegar en Hostinger

## Comandos útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Ver status de migraciones
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Compilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests (cuando estén disponibles)
python manage.py test

# Shell interactivo de Django
python manage.py shell
```

---

**Repositorio**: https://github.com/lcuper18/FPCD  
**Rama principal**: main  
**Última actualización**: 3 de Febrero de 2026
