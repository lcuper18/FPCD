from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para Fe para Cada Día
    Extiende el modelo de usuario de Django
    """
    ROLE_CHOICES = [
        ('reader', 'Lector'),
        ('collaborator', 'Colaborador'),
        ('admin', 'Administrador'),
    ]
    
    email = models.EmailField('correo electrónico', unique=True)
    phone = models.CharField('teléfono', max_length=20, blank=True)
    bio = models.TextField('biografía', blank=True, help_text='Breve descripción sobre ti')
    profile_picture = models.ImageField(
        'foto de perfil',
        upload_to='profiles/',
        blank=True,
        null=True
    )
    role = models.CharField(
        'rol',
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader'
    )
    subscribed_to_newsletter = models.BooleanField(
        'suscrito al newsletter',
        default=False
    )
    created_at = models.DateTimeField('fecha de registro', auto_now_add=True)
    updated_at = models.DateTimeField('última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    @property
    def is_collaborator(self):
        """Verifica si el usuario es colaborador o admin"""
        return self.role in ['collaborator', 'admin']
    
    @property
    def full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
