"""
Modelos para el flujo de trabajo de revisión de contenido.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.content.models import ContentStatus


class ReviewStatus(models.TextChoices):
    """Estados de una revisión."""

    PENDING = "pending", _("Pendiente")
    APPROVED = "approved", _("Aprobado")
    REJECTED = "rejected", _("Rechazado")
    REVISION_REQUIRED = "revision_required", _("Requiere Revisión")


class Review(models.Model):
    """
    Modelo para representar una revisión de contenido.
    """

    content_type = models.CharField(max_length=50, verbose_name=_("Tipo de contenido"))
    content_id = models.PositiveIntegerField(verbose_name=_("ID del contenido"))

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews_given",
        verbose_name=_("Revisor"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received",
        verbose_name=_("Autor del contenido"),
    )

    status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        verbose_name=_("Estado de revisión"),
    )

    comment = models.TextField(blank=True, verbose_name=_("Comentario"))
    feedback = models.TextField(blank=True, verbose_name=_("Feedback"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Revisión")
        verbose_name_plural = _("Revisiones")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "content_id"]),
            models.Index(fields=["reviewer", "status"]),
            models.Index(fields=["author", "status"]),
        ]

    def __str__(self):
        return f"Revisión {self.content_type} #{self.content_id} - {self.get_status_display()}"


class NotificationType(models.TextChoices):
    """Tipos de notificación."""

    CONTENT_SUBMITTED = "content_submitted", _("Contenido enviado a revisión")
    CONTENT_APPROVED = "content_approved", _("Contenido aprobado")
    CONTENT_REJECTED = "content_rejected", _("Contenido rechazado")
    CONTENT_PUBLISHED = "content_published", _("Contenido publicado")
    COMMENT_REPLY = "comment_reply", _("Respuesta a comentario")
    MENTION = "mention", _("Mención")
    SYSTEM = "system", _("Sistema")


class Notification(models.Model):
    """
    Modelo para notificaciones de usuario.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Usuario"),
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        verbose_name=_("Tipo de notificación"),
    )

    title = models.CharField(max_length=200, verbose_name=_("Título"))
    message = models.TextField(verbose_name=_("Mensaje"))

    link = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Enlace"),
    )

    is_read = models.BooleanField(default=False, verbose_name=_("Leída"))
    read_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Fecha de lectura")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )

    class Meta:
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Notificación para {self.user.email}: {self.title}"


class ContentSubmission(models.Model):
    """
    Modelo para rastrear envíos de contenido para revisión.
    """

    content_type = models.CharField(max_length=50, verbose_name=_("Tipo de contenido"))
    content_id = models.PositiveIntegerField(verbose_name=_("ID del contenido"))

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("Autor"),
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de envío")
    )
    reviewed_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Fecha de revisión")
    )

    notes = models.TextField(blank=True, verbose_name=_("Notas del autor"))

    class Meta:
        verbose_name = _("Envío de contenido")
        verbose_name_plural = _("Envíos de contenido")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Envío {self.content_type} #{self.content_id} por {self.author.email}"
