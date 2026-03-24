"""
Modelos para el sistema de comentarios.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


class CommentStatus(models.TextChoices):
    """Estados de un comentario."""

    PENDING = "pending", _("Pendiente")
    APPROVED = "approved", _("Aprobado")
    REJECTED = "rejected", _("Rechazado")
    SPAM = "spam", _("Spam")


class Comment(models.Model):
    """
    Modelo para comentarios con soporte para respuestas anidadas.
    """

    content_type = models.CharField(max_length=50, verbose_name=_("Tipo de contenido"))
    content_id = models.PositiveIntegerField(verbose_name=_("ID del contenido"))

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
        verbose_name=_("Autor"),
    )
    author_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Nombre del comentario (para anonimos)"),
    )
    author_email = models.EmailField(
        blank=True,
        verbose_name=_("Email del comentario (para anonimos)"),
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name=_("Comentario padre"),
    )

    content = models.TextField(verbose_name=_("Contenido"))

    status = models.CharField(
        max_length=20,
        choices=CommentStatus.choices,
        default=CommentStatus.PENDING,
        verbose_name=_("Estado"),
    )

    is_approved = models.BooleanField(default=False, verbose_name=_("Aprobado"))

    # Metadata
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Dirección IP"),
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("User Agent"),
    )

    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "content_id"]),
            models.Index(fields=["author", "status"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Comentario por {self.get_author_name()} en {self.content_type}#{self.content_id}"

    def get_author_name(self):
        """Retorna el nombre del autor."""
        if self.author:
            return self.author.get_short_name()
        return self.author_name or "Anónimo"

    def get_content_object(self):
        """Retorna el objeto de contenido."""
        from django.apps import apps

        model = apps.get_model("content", self.content_type)
        return model.objects.get(pk=self.content_id)

    def get_replies(self):
        """Retorna las respuestas a este comentario."""
        return Comment.objects.filter(parent=self, is_approved=True)

    def has_replies(self):
        """Verifica si tiene respuestas."""
        return Comment.objects.filter(parent=self, is_approved=True).exists()

    def get_status_class(self):
        """Retorna clase CSS según el estado."""
        status_classes = {
            CommentStatus.PENDING: "yellow",
            CommentStatus.APPROVED: "green",
            CommentStatus.REJECTED: "red",
            CommentStatus.SPAM: "gray",
        }
        return status_classes.get(self.status, "gray")


class CommentVote(models.Model):
    """
    Modelo para votos en comentarios (likes).
    """

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name=_("Comentario"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_votes",
        verbose_name=_("Usuario"),
    )
    vote_type = models.CharField(
        max_length=10,
        choices=[
            ("up", "Upvote"),
            ("down", "Downvote"),
        ],
        verbose_name=_("Tipo de voto"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Voto de comentario")
        verbose_name_plural = _("Votos de comentarios")
        unique_together = [["comment", "user"]]

    def __str__(self):
        return f"{self.user.email} voted {self.vote_type} on comment #{self.comment_id}"
