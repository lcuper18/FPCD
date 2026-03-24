"""
Decoradores y mixins para permisos basados en roles.
"""

from functools import wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorador que permite acceso solo a usuarios con roles específicos.

    Uso:
        @role_required(['admin', 'editor'])
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")

            if request.user.role not in allowed_roles and not request.user.is_superuser:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return redirect("public:home")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def admin_required(view_func):
    """
    Decorador que permite acceso solo a administradores.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if not (request.user.role == "admin" or request.user.is_superuser):
            messages.error(request, "Esta acción requiere permisos de administrador.")
            return redirect("public:home")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def editor_required(view_func):
    """
    Decorador que permite acceso a editores y administradores.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if (
            request.user.role not in ["admin", "editor"]
            and not request.user.is_superuser
        ):
            messages.error(request, "Esta acción es exclusiva para editores.")
            return redirect("public:home")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def reviewer_required(view_func):
    """
    Decorador que permite acceso a revisores y administradores.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if (
            request.user.role not in ["admin", "reviewer"]
            and not request.user.is_superuser
        ):
            messages.error(request, "Esta acción es exclusiva para revisores.")
            return redirect("public:home")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


class RoleRequiredMixin:
    """
    Mixin para vistas basadas en clases que requieren roles específicos.
    """

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if (
            request.user.role not in self.allowed_roles
            and not request.user.is_superuser
        ):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect("public:home")

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin para vistas que requieren permisos de administrador.
    """

    allowed_roles = ["admin"]


class EditorRequiredMixin(RoleRequiredMixin):
    """
    Mixin para vistas que requieren permisos de editor.
    """

    allowed_roles = ["admin", "editor"]


class ReviewerRequiredMixin(RoleRequiredMixin):
    """
    Mixin para vistas que requieren permisos de revisor.
    """

    allowed_roles = ["admin", "reviewer"]
