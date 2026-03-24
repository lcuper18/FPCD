"""
Gestor de usuarios personalizado para autenticación por email.
"""

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Gestor personalizado que permite autenticación por email.
    """

    def create_user(
        self, email, first_name="", last_name="", password=None, **extra_fields
    ):
        """
        Crea y guarda un usuario con email y contraseña.
        """
        if not email:
            raise ValueError(_("El correo electrónico es obligatorio"))

        # Normalizar email
        email = self.normalize_email(email)

        # Asignar username si no se proporciona (requerido por Django)
        if not extra_fields.get("username"):
            extra_fields["username"] = email.split("@")[0]

        # Asignar rol por defecto si no se especifica
        if "role" not in extra_fields:
            extra_fields["role"] = "editor"

        # Asignar first_name y last_name
        extra_fields.setdefault("first_name", first_name or "")
        extra_fields.setdefault("last_name", last_name or "")

        # Remover first_name y last_name de extra_fields para evitar duplicados
        extra_fields.pop("first_name", None)
        extra_fields.pop("last_name", None)

        user = self.model(
            email=email,
            first_name=first_name or "",
            last_name=last_name or "",
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name="", last_name="", password=None, **extra_fields
    ):
        """
        Crea y guarda un superusuario con permisos completos.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True."))

        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def get_queryset(self):
        """Retorna el queryset base ordenado por fecha de creación."""
        return super().get_queryset().order_by("-created_at")
