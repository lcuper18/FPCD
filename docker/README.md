# 🐳 Docker - Fe para Cada Día

Archivos de configuración Docker para desarrollo y producción.

## Archivos

- `Dockerfile` - Imagen Docker principal (Python 3.12)
- `docker-compose.prod.yml` - Composición para producción (PostgreSQL)
- `docker-compose.dev.yml` - Composición para desarrollo (SQLite)
- `.dockerignore` - Archivos a ignorar en la imagen

## Uso

### Desarrollo (SQLite)

```bash
docker-compose -f docker-compose.dev.yml up
```

### Producción (PostgreSQL)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Migraciones y datos

```bash
# Migraciones
docker-compose exec web python manage.py migrate

# Datos de prueba
docker-compose exec web python manage.py seed_data

# Crear superuser
docker-compose exec web python manage.py createsuperuser
```

---

**Nota**: Siempre ejecutar desde el directorio raíz del proyecto
