"""
Tests para los modelos de contenido.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.content.models import (
    Category,
    Article,
    Devocional,
    EstudioBiblico,
    BlogPost,
    ContentStatus,
)

User = get_user_model()


class CategoryModelTest(TestCase):
    """Tests para el modelo Category."""

    def test_create_category(self):
        """Test creación de categoría."""
        category = Category.objects.create(name="Test Category", slug="test-category")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.slug, "test-category")
        self.assertTrue(category.is_active)

    def test_category_str(self):
        """Test __str__ de categoría."""
        category = Category.objects.create(name="Bible Study")
        self.assertEqual(str(category), "Bible Study")

    def test_category_slug_auto_generated(self):
        """Test que el slug se genera automáticamente."""
        category = Category.objects.create(name="Mi Categoría")
        self.assertEqual(category.slug, "mi-categoria")

    def test_category_hierarchy(self):
        """Test jerarquía de categorías."""
        parent = Category.objects.create(name="Parent Category")
        child = Category.objects.create(name="Child Category", parent=parent)
        self.assertEqual(child.parent, parent)


class ContentStatusTest(TestCase):
    """Tests para los estados de contenido."""

    def test_content_status_choices(self):
        """Test que todos los estados están disponibles."""
        self.assertEqual(ContentStatus.DRAFT, "draft")
        self.assertEqual(ContentStatus.IN_REVIEW, "in_review")
        self.assertEqual(ContentStatus.PUBLISHED, "published")
        self.assertEqual(ContentStatus.REJECTED, "rejected")
        self.assertEqual(ContentStatus.ARCHIVED, "archived")


class ArticleModelTest(TestCase):
    """Tests para el modelo Article."""

    def setUp(self):
        """Crear usuario de prueba."""
        self.user = User.objects.create_user(
            email="article_author@fpcd.com",
            password="testpass123",
            role="editor",
        )
        self.category = Category.objects.create(name="Artículos", slug="articulos")

    def test_create_article(self):
        """Test creación de artículo."""
        article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            content="Article content here",
            author=self.user,
            category=self.category,
        )
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.status, ContentStatus.DRAFT)
        self.assertEqual(article.author, self.user)

    def test_article_slug_unique(self):
        """Test que el slug es único."""
        Article.objects.create(
            title="Test Article",
            content="Content 1",
            author=self.user,
        )
        article2 = Article.objects.create(
            title="Test Article",
            content="Content 2",
            author=self.user,
        )
        self.assertEqual(article2.slug, "test-article-1")

    def test_article_get_status_display_class(self):
        """Test get_status_display_class."""
        article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.user,
            status=ContentStatus.PUBLISHED,
        )
        self.assertEqual(article.get_status_display_class(), "green")

    def test_article_is_published(self):
        """Test property is_published."""
        article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.user,
            status=ContentStatus.PUBLISHED,
        )
        self.assertTrue(article.is_published)

        article.status = ContentStatus.DRAFT
        self.assertFalse(article.is_published)


class DevocionalModelTest(TestCase):
    """Tests para el modelo Devocional."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="devocional_author@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_devocional(self):
        """Test creación de devocional."""
        devocional = Devocional.objects.create(
            title="Devocional de Hoy",
            slug="devocional-hoy",
            content="Contenido del devocional",
            author=self.user,
            verse_reference="Juan 3:16",
        )
        self.assertEqual(devocional.verse_reference, "Juan 3:16")
        self.assertTrue(devocional.is_daily)


class EstudioBiblicoModelTest(TestCase):
    """Tests para el modelo EstudioBiblico."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="estudio_author@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_estudio(self):
        """Test creación de estudio bíblico."""
        estudio = EstudioBiblico.objects.create(
            title="Estudio de Génesis 1",
            slug="estudio-genesis-1",
            content="Contenido del estudio",
            author=self.user,
            bible_book="Génesis",
            bible_chapter=1,
            bible_verse_start=1,
            bible_verse_end=31,
        )
        self.assertEqual(estudio.bible_book, "Génesis")
        self.assertEqual(estudio.bible_chapter, 1)

    def test_get_bible_reference(self):
        """Test get_bible_reference."""
        estudio = EstudioBiblico.objects.create(
            title="Study",
            content="Content",
            author=self.user,
            bible_book="Génesis",
            bible_chapter=1,
            bible_verse_start=1,
            bible_verse_end=10,
        )
        self.assertEqual(estudio.get_bible_reference(), "Génesis 1:1-10")


class BlogPostModelTest(TestCase):
    """Tests para el modelo BlogPost."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="blog_author@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_blog_post(self):
        """Test creación de entrada de blog."""
        post = BlogPost.objects.create(
            title="Mi Primer Post",
            slug="mi-primer-post",
            content="Contenido del post",
            excerpt="Extracto del post",
            author=self.user,
        )
        self.assertEqual(post.title, "Mi Primer Post")
        self.assertTrue(post.allow_comments)
        self.assertFalse(post.is_pinned)

    def test_blog_post_excerpt(self):
        """Test que el excerpt es opcional."""
        post = BlogPost.objects.create(
            title="Post sin excerpt",
            content="Content",
            author=self.user,
        )
        self.assertEqual(post.excerpt, "")
