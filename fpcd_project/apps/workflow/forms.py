"""
Formularios para el flujo de trabajo.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import FormActions
from .models import Review, Notification


class ReviewForm(forms.ModelForm):
    """Formulario para crear/editar una revisión."""

    class Meta:
        model = Review
        fields = ["status", "comment", "feedback"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "status",
            "comment",
            "feedback",
            FormActions(
                Submit(
                    "submit",
                    _("Enviar revisión"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class QuickReviewForm(forms.Form):
    """Formulario rápido para aprobar/rechazar contenido."""

    action = forms.ChoiceField(
        choices=[
            ("approve", _("Aprobar")),
            ("reject", _("Rechazar")),
            ("request_revision", _("Solicitar revisión")),
        ],
        widget=forms.RadioSelect,
        label=_("Acción"),
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": _("Comentario opcional")}
        ),
        required=False,
        label=_("Comentario"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "action",
            "comment",
            FormActions(
                Submit(
                    "submit", _("Confirmar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class NotificationSettingsForm(forms.Form):
    """Formulario para configurar notificaciones."""

    email_notifications = forms.BooleanField(
        required=False,
        label=_("Recibir notificaciones por correo"),
    )
    content_submitted = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Cuando envíe contenido a revisión"),
    )
    content_approved = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Cuando mi contenido sea aprobado"),
    )
    content_rejected = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Cuando mi contenido sea rechazado"),
    )
    comments = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Cuando alguien comente en mi contenido"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "email_notifications",
            HTML("<hr>"),
            "content_submitted",
            "content_approved",
            "content_rejected",
            "comments",
            FormActions(
                Submit(
                    "submit",
                    _("Guardar preferencias"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )
