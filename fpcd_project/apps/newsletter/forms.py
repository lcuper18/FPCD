"""
Formularios para newsletter.
"""

from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Column
from crispy_forms.bootstrap import FormActions
from .models import Subscriber


class SubscribeForm(forms.Form):
    """
    Formulario de suscripción al newsletter.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": _("Tu correo electrónico"),
                "required": "required",
            }
        ),
        label=_("Correo electrónico"),
        validators=[validate_email],
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": _("Tu nombre (opcional)"),
            }
        ),
        label=_("Nombre"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "email",
            "first_name",
            FormActions(
                Submit(
                    "submit",
                    _("Suscribirse"),
                    css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()

        # Verificar si ya está suscrito
        if Subscriber.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(
                _("Este correo ya está suscrito al newsletter.")
            )

        # Verificar si existe pero está inactivo
        if Subscriber.objects.filter(email__iexact=email, is_active=False).exists():
            # Podríamos ofrecer reactivarlo
            pass

        return email


class UnsubscribeForm(forms.Form):
    """
    Formulario de cancelación de suscripción.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": _("Tu correo electrónico"),
                "required": "required",
            }
        ),
        label=_("Correo electrónico"),
    )
    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "rows": 3,
                "placeholder": _("¿Por qué te cancelas? (opcional)"),
            }
        ),
        label=_("Razón"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "email",
            "reason",
            FormActions(
                Submit(
                    "submit",
                    _("Cancelar suscripción"),
                    css_class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-lg transition duration-200",
                ),
            ),
        )
