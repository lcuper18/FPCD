from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

User = get_user_model()


class Material(models.Model):
    """Materiales cristianos adicionales (estudios, guías, etc.)"""
    TYPE_CHOICES = [
        ('study', 'Estudio Bíblico'),
        ('guide', 'Guía de Oración'),
        ('article', 'Artículo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('ebook', 'E-book'),
    ]
    
    title = models.CharField('título', max_length=200)
    slug = models.SlugField('slug', unique=True, blank=True)
    description = models.TextField('descripción')
    content = RichTextField('contenido', blank=True)
    material_type = models.CharField('tipo de material', max_length=20, choices=TYPE_CHOICES)
    
    # Archivos y enlaces
    file = models.FileField('archivo', upload_to='materials/', blank=True, null=True)
    external_url = models.URLField('URL externa', blank=True, help_text='YouTube, Drive, etc.')
    thumbnail = models.ImageField('miniatura', upload_to='materials/thumbnails/', blank=True, null=True)
    
    # Organización
    category = models.ForeignKey(
        'devotionals.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='categoría'
    )
    tags = models.CharField('etiquetas', max_length=300, blank=True)
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='autor')
    is_featured = models.BooleanField('destacado', default=False)
    is_published = models.BooleanField('publicado', default=True)
    
    # Estadísticas
    downloads = models.PositiveIntegerField('descargas', default=0)
    views = models.PositiveIntegerField('vistas', default=0)
    
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materiales'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Material.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('materials:detail', kwargs={'slug': self.slug})
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
