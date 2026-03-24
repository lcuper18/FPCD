"""
Formularios para la autenticación y gestión de usuarios.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    PasswordChangeForm as BasePasswordChangeForm,
)
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from .models import UserProfile

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    """
    Formulario para la creación de nuevos usuarios.
    """

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Tu nombre"),
            }
        ),
        label=_("Nombre"),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Tu apellido"),
            }
        ),
        label=_("Apellido"),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("correo@ejemplo.com"),
            }
        ),
        label=_("Correo electrónico"),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Mínimo 8 caracteres"),
            }
        ),
        label=_("Contraseña"),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Confirmar contraseña"),
            }
        ),
        label=_("Confirmar contraseña"),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False  # Usar token manualmente en el template
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="w-full md:w-1/2"),
                Column("last_name", css_class="w-full md:w-1/2"),
            ),
            "email",
            "password1",
            "password2",
            FormActions(
                Submit(
                    "submit",
                    _("Crear cuenta"),
                    css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
                css_class="mt-6",
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("Ya existe un usuario con este correo electrónico.")
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class AuthenticationForm(BaseAuthenticationForm):
    """
    Formulario para inicio de sesión.
    """

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("correo@ejemplo.com"),
                "autofocus": True,
            }
        ),
        label=_("Correo electrónico"),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Tu contraseña"),
            }
        ),
        label=_("Contraseña"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "username",
            "password",
            FormActions(
                Submit(
                    "submit",
                    _("Iniciar sesión"),
                    css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
                HTML(
                    '<p class="mt-4 text-center"><a href="{% url \'accounts:password_reset\' %}" class="text-blue-600 hover:text-blue-800 text-sm">¿Olvidaste tu contraseña?</a></p>'
                ),
                css_class="mt-6",
            ),
        )


class UserProfileForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario.
    """

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            }
        ),
        label=_("Nombre"),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            }
        ),
        label=_("Apellido"),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "readonly": "readonly",
            }
        ),
        label=_("Correo electrónico"),
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "rows": 4,
                "placeholder": _("Cuéntanos sobre ti..."),
            }
        ),
        label=_("Biografía"),
        required=False,
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("+52 555 123 4567"),
            }
        ),
        label=_("Teléfono"),
        required=False,
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            }
        ),
        label=_("Avatar"),
        required=False,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "bio", "phone", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="w-full md:w-1/2"),
                Column("last_name", css_class="w-full md:w-1/2"),
            ),
            "email",
            "bio",
            "phone",
            "avatar",
            FormActions(
                Submit(
                    "submit",
                    _("Guardar cambios"),
                    css_class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition duration-200",
                ),
                HTML(
                    '<a href="{% url \'accounts:profile\' %}" class="ml-4 text-gray-600 hover:text-gray-800">Cancelar</a>'
                ),
                css_class="mt-6",
            ),
        )


class UserProfileExtendedForm(forms.ModelForm):
    """
    Formulario para la información extendida del perfil.
    """

    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("Ciudad, País"),
            }
        ),
        label=_("Ubicación"),
        required=False,
    )
    website = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("https://tusitio.com"),
            }
        ),
        label=_("Sitio web"),
        required=False,
    )
    notifications_enabled = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            }
        ),
        label=_("Recibir notificaciones por correo"),
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = ("location", "website", "notifications_enabled")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "location",
            "website",
            "notifications_enabled",
            FormActions(
                Submit(
                    "submit",
                    _("Guardar"),
                    css_class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition duration-200",
                ),
            ),
        )


class CustomPasswordChangeForm(BasePasswordChangeForm):
    """
    Formulario para cambiar la contraseña.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "old_password",
            "new_password1",
            "new_password2",
            FormActions(
                Submit(
                    "submit",
                    _("Cambiar contraseña"),
                    css_class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition duration-200",
                ),
                HTML(
                    '<a href="{% url \'accounts:profile\' %}" class="ml-4 text-gray-600 hover:text-gray-800">Cancelar</a>'
                ),
            ),
        )


class CustomPasswordResetForm(BasePasswordResetForm):
    """
    Formulario para solicitar recuperación de contraseña.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": _("correo@ejemplo.com"),
            }
        ),
        label=_("Correo electrónico"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "email",
            FormActions(
                Submit(
                    "submit",
                    _("Enviar instrucciones"),
                    css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Solo mostrar mensaje genérico para seguridad
        return email


class CustomSetPasswordForm(BaseSetPasswordForm):
    """
    Formulario para establecer nueva contraseña.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "new_password1",
            "new_password2",
            FormActions(
                Submit(
                    "submit",
                    _("Establecer contraseña"),
                    css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
            ),
        )
