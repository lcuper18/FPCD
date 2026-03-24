"""
Vistas para autenticación y gestión de perfiles.
"""

from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile
from .forms import (
    UserCreationForm,
    AuthenticationForm,
    UserProfileForm,
    UserProfileExtendedForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from .permissions import AdminRequiredMixin, EditorRequiredMixin, ReviewerRequiredMixin

User = get_user_model()


class HomeView(TemplateView):
    """Vista de la página de inicio."""

    template_name = "home.html"


class RegisterView(FormView):
    """
    Vista para el registro de nuevos usuarios.
    """

    template_name = "accounts/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("public:home")
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to home."""
        if request.user.is_authenticated and self.redirect_authenticated_user:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path(), self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        # Autenticar y login automático
        user = authenticate(
            email=form.cleaned_data["email"], password=form.cleaned_data["password1"]
        )
        if user:
            login(self.request, user)
            messages.success(
                self.request,
                f"¡Bienvenido {user.get_short_name()}! Tu cuenta ha sido creada exitosamente.",
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Crear cuenta")
        return context


class LoginView(BaseLoginView):
    """
    Vista para inicio de sesión.
    """

    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_success_url(self):
        messages.success(self.request, "¡Bienvenido de nuevo!")
        return reverse_lazy("public:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Iniciar sesión")
        return context


class LogoutView(BaseLogoutView):
    """
    Vista para cerrar sesión.
    """

    next_page = reverse_lazy("public:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Allow GET requests for logout."""
        return self.post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Vista para mostrar el perfil del usuario.
    """

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Mi perfil")
        context["user"] = self.request.user

        # Obtener o crear perfil extendido
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context["profile"] = profile

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar el perfil del usuario.
    """

    template_name = "accounts/profile_edit.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Tu perfil ha sido actualizado correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Editar perfil")

        # También pasar el perfil extendido
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context["profile_form"] = UserProfileExtendedForm(instance=profile)

        return context

    def post(self, request, *args, **kwargs):
        # Procesar ambos formularios
        user_form = self.get_form()
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileExtendedForm(data=request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)


class PasswordChangeView(LoginRequiredMixin, BasePasswordChangeView):
    """
    Vista para cambiar la contraseña.
    """

    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido cambiada correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Cambiar contraseña")
        return context


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """
    Vista que muestra que el cambio de contraseña fue exitoso.
    """

    template_name = "accounts/password_change_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Contraseña cambiada")
        return context


class PasswordResetView(BasePasswordResetView):
    """
    Vista para solicitar recuperación de contraseña.
    """

    template_name = "accounts/password_reset.html"
    form_class = CustomPasswordResetForm
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Recuperar contraseña")
        return context


class PasswordResetDoneView(BasePasswordResetDoneView):
    """
    Vista que muestra que el email de recuperación fue enviado.
    """

    template_name = "accounts/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Correo enviado")
        return context


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    """
    Vista para establecer nueva contraseña.
    """

    template_name = "accounts/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Establecer nueva contraseña")
        return context


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    """
    Vista que muestra que la contraseña fue restablecida.
    """

    template_name = "accounts/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Contraseña restablecida")
        return context


# Vistas de gestión de usuarios (solo admin)


class UserListView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """Lista de usuarios (solo admin)."""

    template_name = "accounts/user_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Gestión de usuarios")
        context["users"] = User.objects.select_related("profile").order_by(
            "-created_at"
        )
        return context


class UserRoleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Actualizar rol de usuario (solo admin)."""

    model = User
    fields = ["role"]
    template_name = "accounts/user_role_update.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, f"Rol de {form.instance.email} actualizado.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Cambiar rol")
        return context
