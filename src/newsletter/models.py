from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscriber(models.Model):
    """Suscriptores al newsletter (incluyendo no registrados)"""
    email = models.EmailField('correo electrónico', unique=True)
    name = models.CharField('nombre', max_length=100, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='usuario',
        related_name='newsletter_subscription'
    )
    is_active = models.BooleanField('activo', default=True)
    subscribed_at = models.DateTimeField('fecha de suscripción', auto_now_add=True)
    unsubscribed_at = models.DateTimeField('fecha de cancelación', null=True, blank=True)
    
    class Meta:
        verbose_name = 'suscriptor'
        verbose_name_plural = 'suscriptores'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class NewsletterCampaign(models.Model):
    """Campañas de newsletter enviadas"""
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('scheduled', 'Programado'),
        ('sent', 'Enviado'),
    ]
    
    title = models.CharField('título', max_length=200)
    subject = models.CharField('asunto del email', max_length=200)
    content = models.TextField('contenido HTML')
    devotional = models.ForeignKey(
        'devotionals.Devotional',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='devocional',
        help_text='Devocional asociado (opcional)'
    )
    status = models.CharField('estado', max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_for = models.DateTimeField('programado para', null=True, blank=True)
    sent_at = models.DateTimeField('enviado en', null=True, blank=True)
    total_recipients = models.PositiveIntegerField('total de destinatarios', default=0)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'campaña de newsletter'
        verbose_name_plural = 'campañas de newsletter'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.status}"
