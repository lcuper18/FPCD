# 🚀 Sprint 1: Sistema de Autenticación y Usuarios

**Duración estimada:** 1-2 semanas  
**Estado:** ✅ COMPLETADO  
**Prerrequisito:** Sprint 0 completado ✅  
**Fecha de inicio:** 6 de Febrero, 2026  
**Fecha de finalización:** 23 de Marzo, 2026

---

## 🎯 Objetivos del Sprint

1. Crear modelo de usuario personalizado (CustomUser)
2. Implementar sistema de roles (Admin, Editor, Revisor)
3. Desarrollar vistas de autenticación (login, logout, registro)
4. Diseñar templates de autenticación
5. Crear sistema de perfiles de usuario
6. Configurar permisos basados en roles
7. Implementar recuperación de contraseña

---

## 📋 Tareas Detalladas

### Tarea 1: Crear App 'accounts'
- [x] Crear app Django `accounts`
- [x] Agregar a INSTALLED_APPS
- [x] Crear estructura de carpetas

### Tarea 2: Modelo CustomUser
- [x] Extender AbstractUser
- [x] Agregar campos personalizados:
  - role (CharField con choices)
  - bio (TextField)
  - avatar (ImageField)
  - created_at, updated_at
- [x] Configurar AUTH_USER_MODEL en settings
- [x] Crear y aplicar migraciones

### Tarea 3: Modelo UserProfile
- [x] Crear modelo Profile (OneToOne con User)
- [x] Campos adicionales:
  - phone (opcional)
  - location (opcional)
  - social_links (JSONField)
  - website (URLField)
- [x] Signal para crear profile automáticamente
- [x] Migrar cambios

### Tarea 4: Sistema de Roles
- [x] Definir choices para roles:
  - ADMIN
  - EDITOR
  - REVIEWER
- [x] Crear mixins para permisos
- [x] Crear decoradores personalizados
- [x] Implementar métodos helper (is_admin, is_editor, etc.)

### Tarea 5: Admin Personalizado
- [x] Registrar CustomUser en admin
- [x] Personalizar UserAdmin
- [x] Registrar UserProfile (inline)
- [x] Agregar filtros por rol
- [x] Agregar acciones personalizadas

### Tarea 6: Formularios de Autenticación
- [x] UserRegistrationForm
- [x] UserLoginForm
- [x] UserProfileForm
- [x] PasswordChangeForm
- [x] PasswordResetForm
- [x] Integrar con Crispy Forms + Tailwind

### Tarea 7: Vistas de Autenticación
- [x] LoginView (CBV)
- [x] LogoutView
- [x] RegisterView
- [x] ProfileView
- [x] ProfileEditView
- [x] PasswordChangeView
- [x] PasswordResetView
- [x] PasswordResetConfirmView

### Tarea 8: URLs de Autenticación
- [x] Crear accounts/urls.py
- [x] Configurar rutas:
  - /accounts/login/
  - /accounts/logout/
  - /accounts/register/
  - /accounts/profile/
  - /accounts/profile/edit/
  - /accounts/password/change/
  - /accounts/password/reset/
- [x] Incluir en config/urls.py

### Tarea 9: Templates de Autenticación
- [x] accounts/login.html
- [x] accounts/register.html
- [x] accounts/profile.html
- [x] accounts/profile_edit.html
- [x] accounts/password_change.html
- [x] accounts/password_reset.html
- [x] accounts/password_reset_confirm.html
- [x] accounts/password_reset_done.html
- [x] accounts/password_reset_complete.html

### Tarea 10: Actualizar Templates Base
- [x] Agregar navbar con links de auth
- [x] Mostrar usuario logueado
- [x] Dropdown con opciones de perfil
- [x] Botones de login/register para no autenticados
- [x] Avatar del usuario

### Tarea 11: Tests
- [x] Tests de modelo CustomUser
- [x] Tests de registro
- [x] Tests de login/logout
- [x] Tests de permisos por rol
- [x] Tests de profile

### Tarea 12: Documentación
- [x] Documentar modelos
- [x] Documentar vistas
- [x] Crear guía de uso de roles
- [x] Actualizar README

---

## 🏗️ Estructura de la App 'accounts'

```
apps/accounts/
├── __init__.py
├── admin.py              # Admin personalizado
├── apps.py
├── forms.py              # Formularios de auth
├── managers.py           # Custom User Manager
├── models.py             # CustomUser y UserProfile
├── signals.py            # Señales (crear profile)
├── permissions.py        # Mixins y decoradores
├── urls.py               # URLs de la app
├── views.py              # Vistas de autenticación
├── migrations/
│   └── __init__.py
├── templates/accounts/   # Templates específicos
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── ...
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_forms.py
```

---

## 💻 Código de Referencia

### CustomUser Model (Ejemplo)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('editor', 'Editor'),
        ('reviewer', 'Revisor'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='editor'
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Usar email para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_editor(self):
        return self.role == 'editor'
    
    def is_reviewer(self):
        return self.role == 'reviewer'
    
    def __str__(self):
        return self.email
```

### Settings Update

```python
# config/settings/base.py

# Agregar en INSTALLED_APPS
LOCAL_APPS = [
    'apps.accounts',
]

# Configurar custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login configuration
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

---

## ✅ Criterios de Aceptación

Al finalizar este sprint, el sistema debe:

- [x] Permitir registro de nuevos usuarios con email
- [x] Permitir login con email y contraseña
- [x] Asignar roles a usuarios
- [x] Mostrar información de perfil
- [x] Permitir edición de perfil
- [x] Recuperación de contraseña funcional
- [x] Permisos básicos por rol implementados
- [x] Panel admin funcional para gestión de usuarios
- [x] Templates responsive y con buen diseño
- [x] Tests unitarios pasando

---

## 🧪 Tests a Implementar

```python
# apps/accounts/tests/test_models.py

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        """Test creación de usuario normal"""
        pass
    
    def test_create_superuser(self):
        """Test creación de superusuario"""
        pass
    
    def test_user_roles(self):
        """Test asignación de roles"""
        pass

# apps/accounts/tests/test_views.py

class RegisterViewTest(TestCase):
    def test_register_success(self):
        """Test registro exitoso"""
        pass
    
    def test_register_duplicate_email(self):
        """Test registro con email duplicado"""
        pass

class LoginViewTest(TestCase):
    def test_login_success(self):
        """Test login exitoso"""
        pass
    
    def test_login_invalid_credentials(self):
        """Test login con credenciales incorrectas"""
        pass
```

---

## 📝 Comandos Útiles para Este Sprint

```bash
# Crear la app accounts
python manage.py startapp accounts apps/accounts

# Crear migraciones después de definir CustomUser
python manage.py makemigrations accounts

# Aplicar migraciones
python manage.py migrate

# Crear usuario de prueba (desde shell)
python manage.py shell
>>> from apps.accounts.models import CustomUser
>>> user = CustomUser.objects.create_user(
...     username='editor1',
...     email='editor@fpcd.com',
...     password='test123',
...     role='editor'
... )

# Ejecutar tests
python manage.py test apps.accounts

# Ejecutar tests con cobertura
coverage run --source='apps/accounts' manage.py test apps.accounts
coverage report
```

---

## 🎨 Diseño de Templates

### Paleta de Colores (TailwindCSS)

- **Primary:** blue-600
- **Secondary:** purple-600
- **Success:** green-600
- **Danger:** red-600
- **Warning:** yellow-600
- **Info:** cyan-600

### Componentes a Crear

1. **Navbar con auth**
   - Logo
   - Links principales
   - Dropdown de usuario (cuando está logueado)
   - Botones Login/Register (cuando no está logueado)

2. **Formularios estilizados**
   - Labels claros
   - Inputs con validación visual
   - Mensajes de error
   - Botones de acción

3. **Cards de perfil**
   - Avatar circular
   - Información del usuario
   - Botón de editar

---

## 📊 Flujo de Autenticación

```
Usuario No Autenticado
    │
    ├── Clic en "Registrarse"
    │   ├── Formulario de registro
    │   ├── Validación
    │   └── Cuenta creada → Login automático
    │
    ├── Clic en "Iniciar Sesión"
    │   ├── Formulario de login (email + password)
    │   ├── Validación de credenciales
    │   └── Sesión iniciada → Redirigir a home
    │
    └── ¿Olvidó su contraseña?
        ├── Ingresa email
        ├── Email enviado con link
        ├── Clic en link
        └── Nueva contraseña establecida

Usuario Autenticado
    │
    ├── Ver perfil
    │   └── Editar perfil
    │       ├── Cambiar avatar
    │       ├── Actualizar bio
    │       └── Guardar cambios
    │
    ├── Cambiar contraseña
    │   ├── Contraseña actual
    │   ├── Nueva contraseña
    │   └── Confirmar nueva contraseña
    │
    └── Cerrar sesión
        └── Redirigir a home
```

---

## 🔐 Permisos y Roles

### Admin
- Acceso completo al sistema
- Gestionar usuarios y roles
- Publicar sin revisión
- Acceder a estadísticas globales

### Editor
- Crear y editar su propio contenido
- Enviar a revisión
- Ver estadísticas de sus artículos

### Revisor
- Ver contenido en revisión
- Aprobar/rechazar publicaciones
- Comentar en revisiones
- No puede crear contenido

---

## 🚀 Siguiente Sprint

Una vez completado el Sprint 1, continuaremos con:

**Sprint 2: Gestión de Contenido**
- Modelos de contenido (Artículo, Devocional, etc.)
- CRUD de contenido
- Categorías y etiquetas
- Editor TinyMCE integrado

---

## 📌 Notas Importantes

- **EMAIL_BACKEND:** En desarrollo usa console backend
- **MEDIA_ROOT:** Configurado para subir avatares
- **USERNAME_FIELD:** Cambiado a 'email' en lugar de 'username'
- **Migraciones:** Hacer ANTES de crear el primer superusuario

---

## 🏆 Resumen del Sprint 1

El Sprint 1 ha sido completado exitosamente. Se han implementado:

- ✅ Sistema de autenticación completo (login, logout, registro)
- ✅ Modelo CustomUser con roles (Admin, Editor, Revisor)
- ✅ Modelo UserProfile con información extendida
- ✅ Sistema de permisos y restricciones por rol
- ✅ Recuperación de contraseña
- ✅ 63 tests unitarios pasando
- ✅ Templates de autenticación con diseño responsive

**Total de archivos creados/modificados:**
- models.py (CustomUser, UserProfile)
- views.py (13 vistas)
- forms.py (7 formularios)
- urls.py (11 rutas)
- admin.py (admin personalizado)
- permissions.py (mixins y decoradores)
- signals.py (creación automática de perfiles)
- managers.py (gestor personalizado)
- 12 templates de autenticación
- 4 archivos de tests

---

**Sprint 1 Completado** 🎉

¿Listo para empezar el Sprint 2?
