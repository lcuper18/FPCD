"""
Modelos para newsletter y suscripciones.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Subscriber(models.Model):
    """
    Modelo para suscriptores del newsletter.
    """

    email = models.EmailField(_("Correo electrónico"), unique=True, db_index=True)
    first_name = models.CharField(_("Nombre"), max_length=100, blank=True)
    is_active = models.BooleanField(
        _("Activo"),
        default=True,
        help_text=_("Indica si el suscriptor recibe los boletines"),
    )
    is_verified = models.BooleanField(
        _("Verificado"),
        default=False,
        help_text=_("Indica si el email ha sido verificado"),
    )
    verification_token = models.CharField(max_length=64, blank=True)
    subscribed_at = models.DateTimeField(_("Fecha de suscripción"), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(
        _("Fecha de cancelación"), null=True, blank=True
    )
    unsubscribed_reason = models.TextField(_("Razón de cancelación"), blank=True)

    class Meta:
        verbose_name = _("Suscriptor")
        verbose_name_plural = _("Suscriptores")
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    """
    Modelo para boletines/newsletter.
    """

    STATUS_CHOICES = [
        ("draft", _("Borrador")),
        ("scheduled", _("Programado")),
        ("sent", _("Enviado")),
        ("cancelled", _("Cancelado")),
    ]

    subject = models.CharField(_("Asunto"), max_length=200)
    content = models.TextField(_("Contenido"))
    content_html = models.TextField(_("Contenido HTML"), blank=True)
    status = models.CharField(
        _("Estado"), max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    sent_at = models.DateTimeField(_("Fecha de envío"), null=True, blank=True)
    scheduled_for = models.DateTimeField(
        _("Programado para"),
        null=True,
        blank=True,
        help_text=_("Fecha y hora programada para el envío"),
    )
    recipient_count = models.PositiveIntegerField(_("Destinatarios"), default=0)
    open_count = models.PositiveIntegerField(_("Aperturas"), default=0)
    click_count = models.PositiveIntegerField(_("Clics"), default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="newsletters",
        verbose_name=_("Creado por"),
    )
    created_at = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Última actualización"), auto_now=True)

    class Meta:
        verbose_name = _("Boletín")
        verbose_name_plural = _("Boletines")
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject


class NewsletterArchive(models.Model):
    """
    Modelo para guardar los boletines enviados (archivo).
    """

    subject = models.CharField(_("Asunto"), max_length=200)
    content_html = models.TextField(_("Contenido HTML"))
    sent_at = models.DateTimeField(_("Fecha de envío"), auto_now_add=True)
    recipient_count = models.PositiveIntegerField(_("Destinatarios"), default=0)
    open_count = models.PositiveIntegerField(_("Aperturas"), default=0)

    class Meta:
        verbose_name = _("Archivo de boletín")
        verbose_name_plural = _("Archivos de boletines")
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.subject} - {self.sent_at.strftime('%d/%m/%Y')}"
