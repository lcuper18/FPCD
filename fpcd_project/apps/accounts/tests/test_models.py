"""
Tests para los modelos de accounts.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Tests para el modelo CustomUser."""

    def test_create_user_with_email(self):
        """Test creación de usuario con email."""
        user = User.objects.create_user(
            email="test@fpcd.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.email, "test@fpcd.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_default_role(self):
        """Test que el rol por defecto es editor."""
        user = User.objects.create_user(
            email="editor@fpcd.com",
            password="testpass123",
        )
        self.assertEqual(user.role, "editor")

    def test_create_user_with_role(self):
        """Test creación de usuario con rol específico."""
        user = User.objects.create_user(
            email="admin@fpcd.com",
            password="testpass123",
            role="admin",
        )
        self.assertEqual(user.role, "admin")

    def test_create_superuser(self):
        """Test creación de superusuario."""
        user = User.objects.create_superuser(
            email="super@fpcd.com",
            password="testpass123",
            first_name="Super",
            last_name="Admin",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, "admin")

    def test_user_str_method(self):
        """Test método __str__ del usuario."""
        user = User.objects.create_user(
            email="string@fpcd.com",
            password="testpass123",
        )
        self.assertEqual(str(user), "string@fpcd.com")

    def test_get_full_name(self):
        """Test get_full_name."""
        user = User.objects.create_user(
            email="name@fpcd.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.get_full_name(), "John Doe")

    def test_get_full_name_without_names(self):
        """Test get_full_name sin nombres."""
        user = User.objects.create_user(
            email="noname@fpcd.com",
            password="testpass123",
        )
        self.assertEqual(user.get_full_name(), "noname@fpcd.com")

    def test_get_short_name(self):
        """Test get_short_name."""
        user = User.objects.create_user(
            email="short@fpcd.com",
            password="testpass123",
            first_name="Jane",
        )
        self.assertEqual(user.get_short_name(), "Jane")

    def test_is_admin_method(self):
        """Test método is_admin."""
        admin = User.objects.create_user(
            email="admin_test@fpcd.com",
            password="testpass123",
            role="admin",
        )
        editor = User.objects.create_user(
            email="editor_test@fpcd.com",
            password="testpass123",
            role="editor",
        )
        self.assertTrue(admin.is_admin())
        self.assertFalse(editor.is_admin())

    def test_is_editor_method(self):
        """Test método is_editor."""
        editor = User.objects.create_user(
            email="editor_test@fpcd.com",
            password="testpass123",
            role="editor",
        )
        reviewer = User.objects.create_user(
            email="reviewer_test@fpcd.com",
            password="testpass123",
            role="reviewer",
        )
        self.assertTrue(editor.is_editor())
        self.assertFalse(reviewer.is_editor())

    def test_is_reviewer_method(self):
        """Test método is_reviewer."""
        reviewer = User.objects.create_user(
            email="reviewer_test@fpcd.com",
            password="testpass123",
            role="reviewer",
        )
        admin = User.objects.create_user(
            email="admin_test@fpcd.com",
            password="testpass123",
            role="admin",
        )
        self.assertTrue(reviewer.is_reviewer())
        self.assertFalse(admin.is_reviewer())

    def test_get_role_display_name(self):
        """Test get_role_display_name."""
        user = User.objects.create_user(
            email="role@fpcd.com",
            password="testpass123",
            role="editor",
        )
        self.assertEqual(user.get_role_display_name(), "Editor")

    def test_unique_email(self):
        """Test que el email es único."""
        User.objects.create_user(
            email="unique@fpcd.com",
            password="testpass123",
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="unique@fpcd.com",
                password="testpass123",
            )


class UserProfileModelTest(TestCase):
    """Tests para el modelo UserProfile."""

    def test_create_user_profile(self):
        """Test creación de perfil de usuario (el perfil se crea automáticamente con el usuario)."""
        user = User.objects.create_user(
            email="profile@fpcd.com",
            password="testpass123",
        )
        # El perfil se crea automáticamente por la señal
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_profile_str_method(self):
        """Test método __str__ del perfil."""
        user = User.objects.create_user(
            email="profile_str@fpcd.com",
            password="testpass123",
        )
        # El perfil se crea automáticamente por la señal
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), "Perfil de profile_str@fpcd.com")

    def test_profile_default_values(self):
        """Test valores por defecto del perfil."""
        user = User.objects.create_user(
            email="default@fpcd.com",
            password="testpass123",
        )
        # El perfil se crea automáticamente por la señal
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.location, "")
        self.assertEqual(profile.website, "")
        self.assertEqual(profile.social_links, {})
        self.assertTrue(profile.notifications_enabled)

    def test_profile_update(self):
        """Test actualización de perfil."""
        user = User.objects.create_user(
            email="update@fpcd.com",
            password="testpass123",
        )
        profile = UserProfile.objects.get(user=user)
        profile.location = "Mexico City"
        profile.website = "https://example.com"
        profile.save()

        # Verificar actualización
        profile.refresh_from_db()
        self.assertEqual(profile.location, "Mexico City")
        self.assertEqual(profile.website, "https://example.com")

    def test_profile_delete_user_cascade(self):
        """Test que al eliminar usuario se elimina el perfil."""
        user = User.objects.create_user(
            email="cascade@fpcd.com",
            password="testpass123",
        )
        profile = UserProfile.objects.get(user=user)
        user_id = user.id
        user.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user_id=user_id)
