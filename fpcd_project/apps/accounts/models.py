"""
Modelos para la gestión de usuarios personalizados.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado con roles y campos adicionales.
    """

    ROLE_CHOICES = [
        ("admin", _("Administrador")),
        ("editor", _("Editor")),
        ("reviewer", _("Revisor")),
    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="editor", verbose_name=_("Rol")
    )
    bio = models.TextField(blank=True, verbose_name=_("Biografía"))
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name=_("Avatar")
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Teléfono"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    # Usar email como campo principal para autenticación
    email = models.EmailField(_("Correo electrónico"), unique=True)

    # Remover username de requerido ya que usaremos email
    username = models.CharField(
        _("Nombre de usuario"),
        max_length=150,
        blank=True,
        help_text=_("Opcional: puede iniciar sesión solo con email"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Usar el gestor personalizado
    objects = UserManager()

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        """Retorna el nombre corto (first_name o email)."""
        return self.first_name or self.email.split("@")[0]

    # Métodos helper para verificar roles
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    def is_editor(self):
        return self.role == "editor"

    def is_reviewer(self):
        return self.role == "reviewer"

    def get_role_display_name(self):
        """Retorna el nombre legible del rol."""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)


class UserProfile(models.Model):
    """
    Perfil adicional del usuario con información extendida.
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Usuario"),
    )
    location = models.CharField(max_length=255, blank=True, verbose_name=_("Ubicación"))
    website = models.URLField(blank=True, verbose_name=_("Sitio web"))
    social_links = models.JSONField(
        blank=True, default=dict, verbose_name=_("Enlaces sociales")
    )
    notifications_enabled = models.BooleanField(
        default=True, verbose_name=_("Notificaciones habilitadas")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")

    def __str__(self):
        return f"Perfil de {self.user.email}"
