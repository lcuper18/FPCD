"""
Modelos para la gestión de archivos multimedia.
"""

import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator


def get_file_upload_path(instance, filename):
    """Generate upload path for media files."""
    ext = filename.split(".")[-1].lower()
    folder = instance.get_file_type()
    return f"media/{folder}/{instance.uploader.id}/{filename}"


class MediaFileType(models.TextChoices):
    """Tipos de archivos multimedia."""

    IMAGE = "image", _("Imagen")
    DOCUMENT = "document", _("Documento")
    VIDEO = "video", _("Video")
    AUDIO = "audio", _("Audio")
    OTHER = "other", _("Otro")


class MediaFile(models.Model):
    """
    Modelo para gestionar archivos subidos.
    """

    file = models.FileField(
        upload_to=get_file_upload_path,
        verbose_name=_("Archivo"),
    )
    filename = models.CharField(max_length=255, verbose_name=_("Nombre del archivo"))
    file_type = models.CharField(
        max_length=20,
        choices=MediaFileType.choices,
        verbose_name=_("Tipo de archivo"),
    )
    mime_type = models.CharField(
        max_length=100, blank=True, verbose_name=_("Tipo MIME")
    )
    file_size = models.PositiveIntegerField(default=0, verbose_name=_("Tamaño (bytes)"))

    # Metadata
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Título"))
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Texto alternativo"),
        help_text=_("Para accesibilidad"),
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Etiquetas"),
        help_text=_("Separadas por coma"),
    )

    # Image specific
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Ancho"))
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Alto"))
    thumbnail = models.ImageField(
        upload_to="media/thumbnails/",
        null=True,
        blank=True,
        verbose_name=_("Miniatura"),
    )

    # Organization
    folder = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Carpeta"),
    )

    # Usage tracking
    used_in = models.TextField(
        blank=True,
        editable=False,
        verbose_name=_("Usado en"),
        help_text=_("IDs de contenido donde se usa este archivo"),
    )

    # Ownership
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_files",
        verbose_name=_("Subido por"),
    )

    # Status
    is_active = models.BooleanField(default=True, verbose_name=_("Activo"))

    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Archivo")
        verbose_name_plural = _("Archivos")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["file_type"]),
            models.Index(fields=["uploader", "file_type"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.filename

    def get_file_type(self):
        """Retorna el tipo de archivo basado en la extensión."""
        if not self.filename:
            return "other"

        ext = os.path.splitext(self.filename)[1].lower().replace(".", "")

        image_exts = ["jpg", "jpeg", "png", "gif", "webp", "svg", "bmp", "ico"]
        doc_exts = [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "txt",
            "rtf",
            "odt",
        ]
        video_exts = ["mp4", "avi", "mov", "wmv", "flv", "webm", "mkv"]
        audio_exts = ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"]

        if ext in image_exts:
            return "image"
        elif ext in doc_exts:
            return "document"
        elif ext in video_exts:
            return "video"
        elif ext in audio_exts:
            return "audio"
        else:
            return "other"

    def get_file_extension(self):
        """Retorna la extensión del archivo."""
        return os.path.splitext(self.filename)[1].lower().replace(".", "")

    def get_file_size_display(self):
        """Retorna el tamaño formateado."""
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_image_tag(self):
        """Retorna una etiqueta img para previsualización."""
        if self.file_type == "image" and self.file:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                self.file.url,
            )
        return ""

    def get_download_url(self):
        """Retorna URL para descargar."""
        if self.file:
            return self.file.url
        return None

    def save(self, *args, **kwargs):
        # Set file type based on extension
        if not self.file_type:
            self.file_type = self.get_file_type()

        # Get file size
        if self.file and not self.file_size:
            self.file_size = self.file.size

        # Get filename
        if not self.filename:
            self.filename = os.path.basename(self.file.name)

        super().save(*args, **kwargs)


class MediaFolder(models.Model):
    """
    Modelo para organizar archivos en carpetas.
    """

    name = models.CharField(max_length=200, verbose_name=_("Nombre"))
    slug = models.SlugField(max_length=210, unique=True, verbose_name=_("Slug"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Carpeta padre"),
    )
    description = models.TextField(blank=True, verbose_name=_("Descripción"))

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="media_folders",
        verbose_name=_("Creado por"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Carpeta")
        verbose_name_plural = _("Carpetas")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_file_count(self):
        """Retorna el número de archivos en esta carpeta."""
        return MediaFile.objects.filter(folder=self.name, is_active=True).count()
