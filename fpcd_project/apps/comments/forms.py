"""
Formularios para comentarios.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions
from .models import Comment


class CommentForm(forms.ModelForm):
    """Formulario para crear comentarios."""

    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "content",
            FormActions(
                Submit(
                    "submit",
                    _("Publicar comentario"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class AnonymousCommentForm(forms.ModelForm):
    """Formulario para comentarios de anonimos."""

    author_name = forms.CharField(
        max_length=100,
        label=_("Nombre"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("Tu nombre")}),
    )
    author_email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": _("Tu correo electrónico")}),
    )

    class Meta:
        model = Comment
        fields = ["author_name", "author_email", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "author_name",
            "author_email",
            "content",
            FormActions(
                Submit(
                    "submit",
                    _("Publicar comentario"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class ReplyForm(forms.ModelForm):
    """Formulario para responder a comentarios."""

    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            "content",
            FormActions(
                Submit(
                    "submit",
                    _("Responder"),
                    css_class="bg-green-600 hover:bg-green-700",
                ),
            ),
        )
