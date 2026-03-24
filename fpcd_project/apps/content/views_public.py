"""
Vistas públicas para el portal.
"""

from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from apps.content.models import (
    Category,
    Article,
    Devocional,
    EstudioBiblico,
    BlogPost,
    ContentStatus,
)
from apps.media_manager.models import MediaFile
from apps.comments.models import Comment, CommentStatus


class HomeView(TemplateView):
    """Página de inicio pública."""

    template_name = "public/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured articles
        context["featured_articles"] = Article.objects.filter(
            status=ContentStatus.PUBLISHED, is_featured=True
        )[:5]

        # Recent articles
        context["recent_articles"] = Article.objects.filter(
            status=ContentStatus.PUBLISHED
        )[:6]

        # Today's devocional
        context["today_devocional"] = (
            Devocional.objects.filter(status=ContentStatus.PUBLISHED, is_daily=True)
            .order_by("-date")
            .first()
        )

        # Recent estudios
        context["recent_estudios"] = EstudioBiblico.objects.filter(
            status=ContentStatus.PUBLISHED
        )[:4]

        # Recent blog posts
        context["recent_blog"] = BlogPost.objects.filter(
            status=ContentStatus.PUBLISHED, is_pinned=True
        )[:3]

        # Categories
        context["categories"] = Category.objects.filter(is_active=True)[:6]

        context["page_title"] = "Inicio"

        return context


class ArticleListView(ListView):
    """Lista de artículos publicados."""

    model = Article
    template_name = "public/article_list.html"
    context_object_name = "articles"
    paginate_by = 12

    def get_queryset(self):
        return Article.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author", "category"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Categories for filter
        context["categories"] = Category.objects.filter(is_active=True)

        # Filter by category
        category_slug = self.kwargs.get("category")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context["current_category"] = category
            context["articles"] = context["articles"].filter(category=category)

        context["page_title"] = "Artículos"

        return context


class ArticleDetailView(DetailView):
    """Detalle de artículo publicado."""

    model = Article
    template_name = "public/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author", "category"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related articles (same category)
        article = self.get_object()
        context["related_articles"] = Article.objects.filter(
            status=ContentStatus.PUBLISHED, category=article.category
        ).exclude(pk=article.pk)[:3]

        context["page_title"] = article.title

        # Comments for the article
        context["article_comments"] = Comment.objects.filter(
            content_type="Article",
            content_id=article.pk,
            is_approved=True,
            parent__isnull=True,
        ).select_related("author").prefetch_related("replies", "replies__author")

        return context


class DevocionalListView(ListView):
    """Lista de devocionales."""

    model = Devocional
    template_name = "public/devocional_list.html"
    context_object_name = "devocionales"
    paginate_by = 12

    def get_queryset(self):
        return Devocional.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author"
        )


class DevocionalDetailView(DetailView):
    """Detalle de devocional."""

    model = Devocional
    template_name = "public/devocional_detail.html"
    context_object_name = "devocional"

    def get_queryset(self):
        return Devocional.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author"
        )


class EstudioListView(ListView):
    """Lista de estudios bíblicos."""

    model = EstudioBiblico
    template_name = "public/estudio_list.html"
    context_object_name = "estudios"
    paginate_by = 12

    def get_queryset(self):
        return EstudioBiblico.objects.filter(
            status=ContentStatus.PUBLISHED
        ).select_related("author")


class EstudioDetailView(DetailView):
    """Detalle de estudio bíblico."""

    model = EstudioBiblico
    template_name = "public/estudio_detail.html"
    context_object_name = "estudio"

    def get_queryset(self):
        return EstudioBiblico.objects.filter(
            status=ContentStatus.PUBLISHED
        ).select_related("author")


class BlogListView(ListView):
    """Lista de entradas de blog."""

    model = BlogPost
    template_name = "public/blog_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        return BlogPost.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author"
        )


class BlogDetailView(DetailView):
    """Detalle de entrada de blog."""

    model = BlogPost
    template_name = "public/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status=ContentStatus.PUBLISHED).select_related(
            "author"
        )


class CategoryListView(ListView):
    """Lista de categorías."""

    model = Category
    template_name = "public/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


from django.shortcuts import get_object_or_404


class CategoryDetailView(DetailView):
    """Contenido por categoría."""

    model = Category
    template_name = "public/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all content for this category
        category = self.get_object()

        context["articles"] = Article.objects.filter(
            status=ContentStatus.PUBLISHED, category=category
        )[:10]

        context["devocionales"] = Devocional.objects.filter(
            status=ContentStatus.PUBLISHED, category=category
        )[:10]

        context["estudios"] = EstudioBiblico.objects.filter(
            status=ContentStatus.PUBLISHED, category=category
        )[:10]

        context["page_title"] = category.name

        return context


class SearchView(TemplateView):
    """Búsqueda pública."""

    template_name = "public/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")
        context["query"] = query

        if query:
            # Search articles
            articles = Article.objects.filter(status=ContentStatus.PUBLISHED).filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )[:10]

            # Search devocionales
            devocionales = Devocional.objects.filter(
                status=ContentStatus.PUBLISHED
            ).filter(Q(title__icontains=query) | Q(content__icontains=query))[:10]

            # Search estudios
            estudios = EstudioBiblico.objects.filter(
                status=ContentStatus.PUBLISHED
            ).filter(Q(title__icontains=query) | Q(content__icontains=query))[:10]

            # Search blog
            blog_posts = BlogPost.objects.filter(status=ContentStatus.PUBLISHED).filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )[:10]

            context["articles"] = articles
            context["devocionales"] = devocionales
            context["estudios"] = estudios
            context["blog_posts"] = blog_posts

            context["total_results"] = (
                len(articles) + len(devocionales) + len(estudios) + len(blog_posts)
            )

        context["page_title"] = f"Buscar: {query}"

        return context


class AboutView(TemplateView):
    """Página sobre nosotros."""

    template_name = "public/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sobre Nosotros"
        return context


class ContactView(TemplateView):
    """Página de contacto."""

    template_name = "public/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contacto"
        return context
