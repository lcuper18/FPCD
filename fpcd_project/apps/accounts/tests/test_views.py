"""
Tests para las vistas de accounts.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class RegisterViewTest(TestCase):
    """Tests para la vista de registro."""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")

    def test_get_register_page(self):
        """Test que la página de registro carga."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_success(self):
        """Test registro exitoso."""
        response = self.client.post(
            self.register_url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "register@fpcd.com",
                "password1": "SecurePass123!",
                "password2": "SecurePass123!",
            },
        )
        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(email="register@fpcd.com").exists())
        # Verificar que fue redirigido (redirect después de registro exitoso)
        self.assertIn(response.status_code, [200, 302])

    def test_register_duplicate_email(self):
        """Test registro con email duplicado."""
        User.objects.create_user(
            email="duplicate@fpcd.com",
            password="TestPass123!",
        )
        response = self.client.post(
            self.register_url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "duplicate@fpcd.com",
                "password1": "SecurePass123!",
                "password2": "SecurePass123!",
            },
        )
        self.assertFalse(User.objects.filter(email="duplicate@fpcd.com").count() > 1)

    def test_register_passwords_mismatch(self):
        """Test registro con contraseñas que no coinciden."""
        response = self.client.post(
            self.register_url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "mismatch@fpcd.com",
                "password1": "Password123!",
                "password2": "Different123!",
            },
        )
        self.assertFalse(User.objects.filter(email="mismatch@fpcd.com").exists())

    def test_register_authenticated_redirect(self):
        """Test que usuario logueado es redirigido."""
        user = User.objects.create_user(
            email="auth@fpcd.com",
            password="TestPass123!",
        )
        self.client.force_login(user)
        response = self.client.get(self.register_url)
        # redirect_authenticated_user = True
        self.assertEqual(response.status_code, 302)


class LoginViewTest(TestCase):
    """Tests para la vista de login."""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse("accounts:login")
        self.user = User.objects.create_user(
            email="login@fpcd.com",
            password="TestPass123!",
        )

    def test_get_login_page(self):
        """Test que la página de login carga."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_success(self):
        """Test login exitoso."""
        response = self.client.post(
            self.login_url,
            {
                "username": "login@fpcd.com",
                "password": "TestPass123!",
            },
        )
        # Verificar que fue redirigido
        self.assertEqual(response.status_code, 302)
        # Verificar que la sesión contiene el usuario
        session = self.client.session
        self.assertEqual(session["_auth_user_id"], str(self.user.pk))

    def test_login_invalid_credentials(self):
        """Test login con credenciales incorrectas."""
        response = self.client.post(
            self.login_url,
            {
                "username": "login@fpcd.com",
                "password": "WrongPass123!",
            },
        )
        # Should return 200 with form errors (not redirect)
        self.assertEqual(response.status_code, 200)

    def test_login_nonexistent_user(self):
        """Test login con usuario inexistente."""
        response = self.client.post(
            self.login_url,
            {
                "username": "nonexistent@fpcd.com",
                "password": "TestPass123!",
            },
        )
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    """Tests para la vista de logout."""

    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("accounts:logout")
        self.user = User.objects.create_user(
            email="logout@fpcd.com",
            password="TestPass123!",
        )

    def test_logout_redirects(self):
        """Test que logout redirige."""
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)


class ProfileViewTest(TestCase):
    """Tests para la vista de perfil."""

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse("accounts:profile")
        self.user = User.objects.create_user(
            email="profile@fpcd.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
        )

    def test_profile_requires_login(self):
        """Test que perfil requiere login."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_shows_user_info(self):
        """Test que el perfil muestra información del usuario."""
        self.client.force_login(self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")


class ProfileEditViewTest(TestCase):
    """Tests para la vista de edición de perfil."""

    def setUp(self):
        self.client = Client()
        self.profile_edit_url = reverse("accounts:profile_edit")
        self.user = User.objects.create_user(
            email="edit@fpcd.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
        )

    def test_profile_edit_requires_login(self):
        """Test que edición de perfil requiere login."""
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_shows_form(self):
        """Test que la página de edición muestra el formulario."""
        self.client.force_login(self.user)
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile_edit.html")


class PasswordChangeViewTest(TestCase):
    """Tests para el cambio de contraseña."""

    def setUp(self):
        self.client = Client()
        self.password_change_url = reverse("accounts:password_change")
        self.user = User.objects.create_user(
            email="password@fpcd.com",
            password="TestPass123!",
        )

    def test_password_change_requires_login(self):
        """Test que cambio de contraseña requiere login."""
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 302)

    def test_password_change_shows_form(self):
        """Test que la página de cambio muestra el formulario."""
        self.client.force_login(self.user)
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 200)


class UserListViewTest(TestCase):
    """Tests para la lista de usuarios (solo admin)."""

    def setUp(self):
        self.client = Client()
        self.user_list_url = reverse("accounts:user_list")
        self.admin = User.objects.create_user(
            email="admin@fpcd.com",
            password="TestPass123!",
            role="admin",
        )
        self.editor = User.objects.create_user(
            email="editor@fpcd.com",
            password="TestPass123!",
            role="editor",
        )

    def test_user_list_requires_admin(self):
        """Test que lista de usuarios requiere admin."""
        self.client.force_login(self.editor)
        response = self.client.get(self.user_list_url)
        # No admin, debe ser redirigido
        self.assertEqual(response.status_code, 302)

    def test_user_list_accessible_by_admin(self):
        """Test que admin puede acceder."""
        self.client.force_login(self.admin)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user_list.html")
