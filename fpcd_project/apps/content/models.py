"""
Modelos para la gestión de contenido.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from taggit.managers import TaggableManager
from slugify import slugify


class Category(models.Model):
    """
    Modelo para categorías de contenido.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))
    slug = models.SlugField(max_length=110, unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Categoría padre"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Activa"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:category", kwargs={"slug": self.slug})


class ContentStatus(models.TextChoices):
    """Estados posibles del contenido."""

    DRAFT = "draft", _("Borrador")
    IN_REVIEW = "in_review", _("En Revisión")
    PUBLISHED = "published", _("Publicado")
    REJECTED = "rejected", _("Rechazado")
    ARCHIVED = "archived", _("Archivado")


class ContentBase(models.Model):
    """
    Modelo base abstracto para todo el contenido.
    Proporciona campos comunes a todos los tipos de contenido.
    """

    title = models.CharField(max_length=200, verbose_name=_("Título"))
    slug = models.SlugField(max_length=210, unique=True, verbose_name=_("Slug"))
    content = models.TextField(verbose_name=_("Contenido"))

    # Autor y estado
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_posts",
        verbose_name=_("Autor"),
    )
    status = models.CharField(
        max_length=20,
        choices=ContentStatus.choices,
        default=ContentStatus.DRAFT,
        verbose_name=_("Estado"),
    )

    # Categorización
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_posts",
        verbose_name=_("Categoría"),
    )
    tags = TaggableManager(verbose_name=_("Etiquetas"), blank=True)

    # Imagen destacada
    featured_image = models.ImageField(
        upload_to="content/featured/%Y/%m/",
        blank=True,
        null=True,
        verbose_name=_("Imagen destacada"),
    )

    # SEO
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        verbose_name=_("Meta título"),
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Meta descripción"),
    )

    # Fechas
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de publicación"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    # Estadísticas
    views = models.PositiveIntegerField(default=0, verbose_name=_("Vistas"))

    class Meta:
        abstract = True
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-published_at"]),
            models.Index(fields=["-views"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            # Ensure unique slug
            queryset = self.__class__.objects.filter(slug__startswith=base_slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            f"content:{self.__class__.__name__.lower()}_detail",
            kwargs={"slug": self.slug},
        )

    def get_status_display_class(self):
        """Retorna clase CSS según el estado."""
        status_classes = {
            ContentStatus.DRAFT: "gray",
            ContentStatus.IN_REVIEW: "yellow",
            ContentStatus.PUBLISHED: "green",
            ContentStatus.REJECTED: "red",
            ContentStatus.ARCHIVED: "gray",
        }
        return status_classes.get(self.status, "gray")

    @property
    def is_published(self):
        return self.status == ContentStatus.PUBLISHED


class Article(ContentBase):
    """
    Modelo para artículos bíblicos.
    """

    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Subtítulo"),
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Articulo destacado"),
    )
    read_time = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Tiempo de lectura (minutos)"),
    )

    class Meta(ContentBase.Meta):
        verbose_name = _("Artículo")
        verbose_name_plural = _("Artículos")


class Devocional(ContentBase):
    """
    Modelo para devocionales diarios.
    """

    verse_reference = models.CharField(
        max_length=200,
        verbose_name=_("Referencia bíblica"),
    )
    verse_text = models.TextField(
        blank=True,
        verbose_name=_("Texto del versículo"),
    )
    is_daily = models.BooleanField(
        default=True,
        verbose_name=_("Devocional del día"),
    )
    date = models.DateField(
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Fecha del devocional"),
    )

    class Meta(ContentBase.Meta):
        verbose_name = _("Devocional")
        verbose_name_plural = _("Devocionales")
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        # Set date to today if not set and it's a daily devotional
        if self.is_daily and not self.date:
            from django.utils import timezone

            self.date = timezone.now().date()
        super().save(*args, **kwargs)


class EstudioBiblico(ContentBase):
    """
    Modelo para estudios bíblicos.
    """

    bible_book = models.CharField(
        max_length=100,
        verbose_name=_("Libro bíblico"),
    )
    bible_chapter = models.PositiveIntegerField(
        verbose_name=_("Capítulo"),
    )
    bible_verse_start = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Versículo inicial"),
    )
    bible_verse_end = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Versículo final"),
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", _("Principiante")),
            ("intermediate", _("Intermedio")),
            ("advanced", _("Avanzado")),
        ],
        default="beginner",
        verbose_name=_("Dificultad"),
    )
    duration = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Duración (minutos)"),
    )

    class Meta(ContentBase.Meta):
        verbose_name = _("Estudio Bíblico")
        verbose_name_plural = _("Estudios Bíblicos")

    def get_bible_reference(self):
        """Retorna la referencia bíblica formateada."""
        ref = f"{self.bible_book} {self.bible_chapter}"
        if self.bible_verse_start:
            ref += f":{self.bible_verse_start}"
            if self.bible_verse_end and self.bible_verse_end != self.bible_verse_start:
                ref += f"-{self.bible_verse_end}"
        return ref


class BlogPost(ContentBase):
    """
    Modelo para entradas de blog.
    """

    excerpt = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Extracto"),
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name=_("Fijo en inicio"),
    )
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("Permitir comentarios"),
    )

    class Meta(ContentBase.Meta):
        verbose_name = _("Entrada de Blog")
        verbose_name_plural = _("Entradas de Blog")
