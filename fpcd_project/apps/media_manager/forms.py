"""
Formularios para la gestión de medios.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Hidden
from crispy_forms.bootstrap import FormActions
from .models import MediaFile, MediaFolder
from apps.media_manager.models import MediaFileType


class MediaFileUploadForm(forms.ModelForm):
    """Formulario para subir archivos."""

    class Meta:
        model = MediaFile
        fields = ["file", "title", "description", "alt_text", "tags", "folder"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            "file",
            HTML("""
                <div id="upload-progress" class="hidden mb-4">
                    <div class="w-full bg-gray-200 rounded-full">
                        <div id="progress-bar" class="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full" style="width: 0%">0%</div>
                    </div>
                    <p class="text-sm text-gray-500 mt-1">Subiendo...</p>
                </div>
            """),
            "title",
            "description",
            "alt_text",
            "tags",
            "folder",
            FormActions(
                Submit(
                    "submit",
                    _("Subir archivo"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class MediaFileEditForm(forms.ModelForm):
    """Formulario para editar metadatos de archivo."""

    class Meta:
        model = MediaFile
        fields = ["title", "description", "alt_text", "tags", "folder", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "title",
            "description",
            "alt_text",
            "tags",
            "folder",
            "is_active",
            FormActions(
                Submit(
                    "submit",
                    _("Guardar cambios"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class MediaFolderForm(forms.ModelForm):
    """Formulario para carpetas."""

    class Meta:
        model = MediaFolder
        fields = ["name", "slug", "parent", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "name",
            "slug",
            "parent",
            "description",
            FormActions(
                Submit(
                    "submit",
                    _("Crear carpeta"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )


class MediaSearchForm(forms.Form):
    """Formulario para buscar archivos."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Buscar archivos...")}),
        label=_("Buscar"),
    )
    file_type = forms.ChoiceField(
        required=False,
        choices=[("", _("Todos los tipos"))] + list(MediaFileType.choices),
        label=_("Tipo de archivo"),
    )
    folder = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=_("Carpeta"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "flex gap-4"
        self.helper.layout = Layout(
            "search",
            "file_type",
            "folder",
            Submit("submit", _("Buscar"), css_class="bg-gray-600 hover:bg-gray-700"),
        )
