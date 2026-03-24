"""
Tests para los permisos de accounts.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RolePermissionsTest(TestCase):
    """Tests para verificar permisos por rol."""

    def setUp(self):
        self.client = Client()

        # Crear usuarios de cada rol
        self.admin = User.objects.create_user(
            email="perm_admin@fpcd.com",
            password="TestPass123!",
            role="admin",
        )
        self.editor = User.objects.create_user(
            email="perm_editor@fpcd.com",
            password="TestPass123!",
            role="editor",
        )
        self.reviewer = User.objects.create_user(
            email="perm_reviewer@fpcd.com",
            password="TestPass123!",
            role="reviewer",
        )

        # URL protegida
        self.user_list_url = reverse("accounts:user_list")

    def test_admin_has_access_to_admin_views(self):
        """Test que admin puede acceder a vistas de admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 200)

    def test_editor_denied_admin_views(self):
        """Test que editor no puede acceder a vistas de admin."""
        self.client.force_login(self.editor)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 302)

    def test_reviewer_denied_admin_views(self):
        """Test que reviewer no puede acceder a vistas de admin."""
        self.client.force_login(self.reviewer)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirect_to_login(self):
        """Test que usuario no autenticado es redirigido a login."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class RoleMethodsTest(TestCase):
    """Tests para los métodos de verificación de rol."""

    def test_is_admin_with_admin_role(self):
        """Test is_admin con rol admin."""
        user = User.objects.create_user(
            email="role_admin@fpcd.com",
            password="TestPass123!",
            role="admin",
        )
        self.assertTrue(user.is_admin())

    def test_is_admin_with_superuser(self):
        """Test is_admin con superuser."""
        user = User.objects.create_superuser(
            email="superuser@fpcd.com",
            password="TestPass123!",
        )
        self.assertTrue(user.is_admin())

    def test_is_admin_with_other_role(self):
        """Test is_admin con otro rol."""
        user = User.objects.create_user(
            email="role_other@fpcd.com",
            password="TestPass123!",
            role="editor",
        )
        self.assertFalse(user.is_admin())

    def test_is_editor_with_editor_role(self):
        """Test is_editor con rol editor."""
        user = User.objects.create_user(
            email="role_editor_test@fpcd.com",
            password="TestPass123!",
            role="editor",
        )
        self.assertTrue(user.is_editor())

    def test_is_editor_with_admin_role(self):
        """Test is_editor con rol admin."""
        user = User.objects.create_user(
            email="admin_editor@fpcd.com",
            password="TestPass123!",
            role="admin",
        )
        # Admin no es editor por defecto
        self.assertFalse(user.is_editor())

    def test_is_reviewer_with_reviewer_role(self):
        """Test is_reviewer con rol reviewer."""
        user = User.objects.create_user(
            email="role_reviewer_test@fpcd.com",
            password="TestPass123!",
            role="reviewer",
        )
        self.assertTrue(user.is_reviewer())

    def test_get_role_display_name_admin(self):
        """Test get_role_display_name para admin."""
        user = User.objects.create_user(
            email="display_admin@fpcd.com",
            password="TestPass123!",
            role="admin",
        )
        self.assertEqual(user.get_role_display_name(), "Administrador")

    def test_get_role_display_name_editor(self):
        """Test get_role_display_name para editor."""
        user = User.objects.create_user(
            email="display_editor@fpcd.com",
            password="TestPass123!",
            role="editor",
        )
        self.assertEqual(user.get_role_display_name(), "Editor")

    def test_get_role_display_name_reviewer(self):
        """Test get_role_display_name para reviewer."""
        user = User.objects.create_user(
            email="display_reviewer@fpcd.com",
            password="TestPass123!",
            role="reviewer",
        )
        self.assertEqual(user.get_role_display_name(), "Revisor")
