from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

User = get_user_model()


class Category(models.Model):
    """Categorías para organizar devocionales y materiales"""
    name = models.CharField('nombre', max_length=100, unique=True)
    slug = models.SlugField('slug', unique=True, blank=True)
    description = models.TextField('descripción', blank=True)
    icon = models.CharField('icono', max_length=50, blank=True, help_text='Emoji o clase CSS')
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Devotional(models.Model):
    """Modelo para devocionales diarios"""
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('scheduled', 'Programado'),
    ]
    
    title = models.CharField('título', max_length=200)
    slug = models.SlugField('slug', unique=True, blank=True)
    subtitle = models.CharField('subtítulo', max_length=300, blank=True)
    
    # Versículo principal
    bible_verse = models.CharField('versículo bíblico', max_length=500)
    bible_reference = models.CharField('referencia bíblica', max_length=100, help_text='Ej: Juan 3:16')
    
    # Contenido
    content = RichTextField('contenido')
    reflection = RichTextField('reflexión', blank=True)
    prayer = models.TextField('oración', blank=True)
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='autor', related_name='devotionals')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='categoría')
    tags = models.CharField('etiquetas', max_length=300, blank=True, help_text='Separadas por comas')
    
    # Imagen destacada
    featured_image = models.ImageField('imagen destacada', upload_to='devotionals/', blank=True, null=True)
    
    # Estado y fechas
    status = models.CharField('estado', max_length=20, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateField('fecha de publicación')
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('última actualización', auto_now=True)
    
    # Estadísticas
    views = models.PositiveIntegerField('vistas', default=0)
    
    class Meta:
        verbose_name = 'devocional'
        verbose_name_plural = 'devocionales'
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.publish_date}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Devotional.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('devotionals:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Incrementa el contador de vistas"""
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def tag_list(self):
        """Retorna lista de tags"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Comment(models.Model):
    """Comentarios en devocionales"""
    devotional = models.ForeignKey(Devotional, on_delete=models.CASCADE, related_name='comments', verbose_name='devocional')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuario')
    content = models.TextField('contenido')
    is_approved = models.BooleanField('aprobado', default=False)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comentario de {self.user.username} en {self.devotional.title}"


class Favorite(models.Model):
    """Devocionales favoritos de usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='usuario')
    devotional = models.ForeignKey(Devotional, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='devocional')
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'favorito'
        verbose_name_plural = 'favoritos'
        unique_together = ['user', 'devotional']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.devotional.title}"
