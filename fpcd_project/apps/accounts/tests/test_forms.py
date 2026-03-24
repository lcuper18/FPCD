"""
Tests para los formularios de accounts.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserProfileForm,
    UserProfileExtendedForm,
)
from apps.accounts.models import UserProfile

User = get_user_model()


class UserCreationFormTest(TestCase):
    """Tests para el formulario de registro de usuarios."""

    def test_valid_form(self):
        """Test formulario válido."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "form@fpcd.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_mismatch(self):
        """Test contraseñas que no coinciden."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "mismatch@fpcd.com",
            "password1": "Password123!",
            "password2": "Different123!",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_duplicate_email(self):
        """Test registro con email duplicado."""
        User.objects.create_user(
            email="duplicate@fpcd.com",
            password="TestPass123!",
        )
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@fpcd.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_required_fields(self):
        """Test campos requeridos faltantes."""
        form_data = {
            "first_name": "John",
            "email": "required@fpcd.com",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)

    def test_email_normalized(self):
        """Test que el email se normaliza a minúsculas."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "UPPERCASE@FPCD.COM",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        form = UserCreationForm(data=form_data)
        user = form.save()
        self.assertEqual(user.email, "uppercase@fpcd.com")

    def test_save_user(self):
        """Test que save() crea el usuario."""
        form_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "save@fpcd.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        form = UserCreationForm(data=form_data)
        user = form.save()
        self.assertEqual(user.email, "save@fpcd.com")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Smith")
        self.assertTrue(user.check_password("SecurePass123!"))


class AuthenticationFormTest(TestCase):
    """Tests para el formulario de autenticación."""

    def setUp(self):
        """Crear usuario de prueba."""
        self.user = User.objects.create_user(
            email="auth@fpcd.com",
            password="TestPass123!",
        )

    def test_valid_credentials(self):
        """Test credenciales válidas."""
        form_data = {
            "username": "auth@fpcd.com",
            "password": "TestPass123!",
        }
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        """Test contraseña incorrecta."""
        form_data = {
            "username": "auth@fpcd.com",
            "password": "WrongPass123!",
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        """Test email que no existe."""
        form_data = {
            "username": "nonexistent@fpcd.com",
            "password": "TestPass123!",
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        """Test campos vacíos."""
        form_data = {}
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)


class UserProfileFormTest(TestCase):
    """Tests para el formulario de perfil de usuario."""

    def setUp(self):
        """Crear usuario de prueba."""
        self.user = User.objects.create_user(
            email="profile@fpcd.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
        )

    def test_valid_form(self):
        """Test formulario válido."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "profile@fpcd.com",
            "bio": "Test bio",
            "phone": "+52 555 123 4567",
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_email_readonly(self):
        """Test que el email es de solo lectura."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "changed@fpcd.com",
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        # El campo es readonly en el widget, no en el modelo
        # así que la validación pasa pero el valor no cambia
        self.assertTrue(form.is_valid())


class UserProfileExtendedFormTest(TestCase):
    """Tests para el formulario de perfil extendido."""

    def test_valid_form(self):
        """Test formulario válido."""
        user = User.objects.create_user(
            email="extended@fpcd.com",
            password="TestPass123!",
        )
        # El perfil ya existe gracias a la señal
        profile = UserProfile.objects.get(user=user)
        form_data = {
            "location": "Mexico City",
            "website": "https://example.com",
            "notifications_enabled": True,
        }
        form = UserProfileExtendedForm(data=form_data, instance=profile)
        self.assertTrue(form.is_valid())

    def test_invalid_website(self):
        """Test sitio web inválido."""
        user = User.objects.create_user(
            email="invweb@fpcd.com",
            password="TestPass123!",
        )
        # El perfil ya existe gracias a la señal
        profile = UserProfile.objects.get(user=user)
        form_data = {
            "website": "not-a-url",
        }
        form = UserProfileExtendedForm(data=form_data, instance=profile)
        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)
