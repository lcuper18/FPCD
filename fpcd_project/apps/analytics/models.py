"""
Modelos para analíticas y estadísticas.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PageView(models.Model):
    """
    Modelo para registrar cada visita a una página.
    """

    CONTENT_TYPE_CHOICES = [
        ("article", _("Artículo")),
        ("devocional", _("Devocional")),
        ("estudio", _("Estudio bíblico")),
        ("blog", _("Entrada de blog")),
    ]

    content_type = models.CharField(
        _("Tipo de contenido"), max_length=20, choices=CONTENT_TYPE_CHOICES
    )
    object_id = models.PositiveIntegerField(_("ID del objeto"))

    # Generic foreign key for flexible content reference
    content_type_obj = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    content_object = GenericForeignKey("content_type_obj", "object_id")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="page_views",
        verbose_name=_("Usuario"),
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(_("Dirección IP"), null=True, blank=True)
    user_agent = models.CharField(_("User Agent"), max_length=500, blank=True)
    referrer = models.URLField(_("Referente"), max_length=500, blank=True)
    viewed_at = models.DateTimeField(
        _("Fecha de visita"), auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = _("Vista de página")
        verbose_name_plural = _("Vistas de páginas")
        ordering = ["-viewed_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id", "-viewed_at"]),
            models.Index(fields=["-viewed_at"]),
        ]

    def __str__(self):
        return f"{self.content_type} #{self.object_id} - {self.viewed_at}"


class DailyStats(models.Model):
    """
    Estadísticas diarias agregadas.
    """

    date = models.DateField(_("Fecha"), unique=True, db_index=True)
    total_views = models.PositiveIntegerField(_("Total de visitas"), default=0)
    unique_visitors = models.PositiveIntegerField(_("Visitantes únicos"), default=0)
    article_views = models.PositiveIntegerField(_("Vistas de artículos"), default=0)
    devotional_views = models.PositiveIntegerField(
        _("Vistas de devocionales"), default=0
    )
    study_views = models.PositiveIntegerField(_("Vistas de estudios"), default=0)
    blog_views = models.PositiveIntegerField(_("Vistas de blog"), default=0)
    new_subscribers = models.PositiveIntegerField(_("Nuevos suscriptores"), default=0)

    class Meta:
        verbose_name = _("Estadística diaria")
        verbose_name_plural = _("Estadísticas diarias")
        ordering = ["-date"]

    def __str__(self):
        return f"Stats for {self.date}"


class ContentStats(models.Model):
    """
    Estadísticas por contenido.
    """

    content_type = models.CharField(_("Tipo de contenido"), max_length=20)
    object_id = models.PositiveIntegerField()

    # Generic foreign key
    content_type_obj = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    content_object = GenericForeignKey("content_type_obj", "object_id")

    total_views = models.PositiveIntegerField(_("Total de vistas"), default=0)
    unique_views = models.PositiveIntegerField(_("Vistas únicas"), default=0)
    last_viewed = models.DateTimeField(_("Última vista"), null=True, blank=True)

    class Meta:
        verbose_name = _("Estadística de contenido")
        verbose_name_plural = _("Estadísticas de contenido")
        unique_together = ["content_type", "object_id"]

    def __str__(self):
        return f"{self.content_type} #{self.object_id}: {self.total_views} views"
