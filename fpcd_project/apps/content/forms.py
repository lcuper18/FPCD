"""
Formularios para la gestión de contenido.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from .models import (
    Category,
    Article,
    Devocional,
    EstudioBiblico,
    BlogPost,
    ContentStatus,
)


class CategoryForm(forms.ModelForm):
    """Formulario para categorías."""

    class Meta:
        model = Category
        fields = ["name", "slug", "description", "parent", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="w-full md:w-1/2"),
                Column("slug", css_class="w-full md:w-1/2"),
            ),
            "description",
            "parent",
            "is_active",
            FormActions(
                Submit(
                    "submit", _("Guardar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class ContentFormMixin:
    """Mixin para formularios de contenido."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"

        # Add TinyMCE to content field
        self.helper[("content")].wrap(lambda field: field)


class ArticleForm(forms.ModelForm):
    """Formulario para artículos."""

    class Meta:
        model = Article
        fields = [
            "title",
            "subtitle",
            "slug",
            "content",
            "author",
            "status",
            "category",
            "tags",
            "featured_image",
            "meta_title",
            "meta_description",
            "is_featured",
            "read_time",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _("Contenido"),
                    "title",
                    "subtitle",
                    "slug",
                    "content",
                ),
                Tab(
                    _("Organización"),
                    "author",
                    "status",
                    "category",
                    "tags",
                ),
                Tab(
                    _("Opciones"),
                    "is_featured",
                    "read_time",
                ),
                Tab(
                    _("Imagen y SEO"),
                    "featured_image",
                    "meta_title",
                    "meta_description",
                    css_class="collapse",
                ),
            ),
            FormActions(
                Submit(
                    "submit", _("Guardar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class DevocionalForm(forms.ModelForm):
    """Formulario para devocionales."""

    class Meta:
        model = Devocional
        fields = [
            "title",
            "slug",
            "content",
            "author",
            "status",
            "category",
            "tags",
            "featured_image",
            "meta_title",
            "meta_description",
            "verse_reference",
            "verse_text",
            "is_daily",
            "date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _("Contenido"),
                    "title",
                    "slug",
                    "content",
                ),
                Tab(
                    _("Organización"),
                    "author",
                    "status",
                    "category",
                    "tags",
                ),
                Tab(
                    _("Devocional"),
                    "verse_reference",
                    "verse_text",
                    "is_daily",
                    "date",
                ),
                Tab(
                    _("Imagen y SEO"),
                    "featured_image",
                    "meta_title",
                    "meta_description",
                ),
            ),
            FormActions(
                Submit(
                    "submit", _("Guardar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class EstudioBiblicoForm(forms.ModelForm):
    """Formulario para estudios bíblicos."""

    class Meta:
        model = EstudioBiblico
        fields = [
            "title",
            "slug",
            "content",
            "author",
            "status",
            "category",
            "tags",
            "featured_image",
            "meta_title",
            "meta_description",
            "bible_book",
            "bible_chapter",
            "bible_verse_start",
            "bible_verse_end",
            "difficulty",
            "duration",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _("Contenido"),
                    "title",
                    "slug",
                    "content",
                ),
                Tab(
                    _("Organización"),
                    "author",
                    "status",
                    "category",
                    "tags",
                ),
                Tab(
                    _("Referencia bíblica"),
                    "bible_book",
                    "bible_chapter",
                    "bible_verse_start",
                    "bible_verse_end",
                    "difficulty",
                    "duration",
                ),
                Tab(
                    _("Imagen y SEO"),
                    "featured_image",
                    "meta_title",
                    "meta_description",
                ),
            ),
            FormActions(
                Submit(
                    "submit", _("Guardar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class BlogPostForm(forms.ModelForm):
    """Formulario para entradas de blog."""

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "author",
            "status",
            "category",
            "tags",
            "featured_image",
            "meta_title",
            "meta_description",
            "is_pinned",
            "allow_comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _("Contenido"),
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                ),
                Tab(
                    _("Organización"),
                    "author",
                    "status",
                    "category",
                    "tags",
                ),
                Tab(
                    _("Opciones"),
                    "is_pinned",
                    "allow_comments",
                ),
                Tab(
                    _("Imagen y SEO"),
                    "featured_image",
                    "meta_title",
                    "meta_description",
                ),
            ),
            FormActions(
                Submit(
                    "submit", _("Guardar"), css_class="bg-blue-600 hover:bg-blue-700"
                ),
            ),
        )


class ContentStatusForm(forms.Form):
    """Formulario para cambiar el estado del contenido."""

    status = forms.ChoiceField(choices=ContentStatus.choices)
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        label=_("Comentario"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "status",
            "comment",
            FormActions(
                Submit(
                    "submit",
                    _("Actualizar estado"),
                    css_class="bg-blue-600 hover:bg-blue-700",
                ),
            ),
        )
