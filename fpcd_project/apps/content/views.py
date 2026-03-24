"""
Vistas para la gestión de contenido.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
)
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse

from .models import (
    Category,
    Article,
    Devocional,
    EstudioBiblico,
    BlogPost,
    ContentStatus,
)
from .forms import (
    CategoryForm,
    ArticleForm,
    DevocionalForm,
    EstudioBiblicoForm,
    BlogPostForm,
)
from apps.accounts.permissions import (
    EditorRequiredMixin,
    AdminRequiredMixin,
    ReviewerRequiredMixin,
)


class ContentListView(EditorRequiredMixin, ListView):
    """Vista base para listar contenido."""

    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by status if provided
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        # Filter by category
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category_id=category)
        # Filter by author for editors (not admin)
        if not self.request.user.is_admin():
            queryset = queryset.filter(author=self.request.user)
        return queryset


class ArticleListView(ContentListView):
    """Lista de artículos."""

    model = Article
    template_name = "content/article_list.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Artículos")
        context["status_choices"] = ContentStatus.choices
        return context


class DevocionalListView(ContentListView):
    """Lista de devocionales."""

    model = Devocional
    template_name = "content/devocional_list.html"
    context_object_name = "devocionales"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Devocionales")
        return context


class EstudioBiblicoListView(ContentListView):
    """Lista de estudios bíblicos."""

    model = EstudioBiblico
    template_name = "content/estudio_list.html"
    context_object_name = "estudios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Estudios Bíblicos")
        return context


class BlogPostListView(ContentListView):
    """Lista de entradas de blog."""

    model = BlogPost
    template_name = "content/blog_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Blog")
        return context


class ContentDetailView(DetailView):
    """Vista base para ver detalle de contenido."""

    def get_queryset(self):
        # Only show published content to anonymous users
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(status=ContentStatus.PUBLISHED)

    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj


class ArticleDetailView(ContentDetailView):
    """Detalle de artículo."""

    model = Article
    template_name = "content/article_detail.html"
    context_object_name = "article"


class DevocionalDetailView(ContentDetailView):
    """Detalle de devocional."""

    model = Devocional
    template_name = "content/devocional_detail.html"
    context_object_name = "devocional"


class EstudioBiblicoDetailView(ContentDetailView):
    """Detalle de estudio bíblico."""

    model = EstudioBiblico
    template_name = "content/estudio_detail.html"
    context_object_name = "estudio"


class BlogPostDetailView(ContentDetailView):
    """Detalle de entrada de blog."""

    model = BlogPost
    template_name = "content/blog_detail.html"
    context_object_name = "post"


class ContentCreateView(EditorRequiredMixin, CreateView):
    """Vista base para crear contenido."""

    def form_valid(self, form):
        # Set author to current user
        form.instance.author = self.request.user
        messages.success(self.request, _("Contenido creado exitosamente."))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(f"content:{self.object.__class__.__name__.lower()}_list")


class ArticleCreateView(ContentCreateView):
    """Crear artículo."""

    model = Article
    form_class = ArticleForm
    template_name = "content/article_form.html"


class DevocionalCreateView(ContentCreateView):
    """Crear devocional."""

    model = Devocional
    form_class = DevocionalForm
    template_name = "content/devocional_form.html"


class EstudioBiblicoCreateView(ContentCreateView):
    """Crear estudio bíblico."""

    model = EstudioBiblico
    form_class = EstudioBiblicoForm
    template_name = "content/estudio_form.html"


class BlogPostCreateView(ContentCreateView):
    """Crear entrada de blog."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "content/blog_form.html"


class ContentUpdateView(EditorRequiredMixin, UpdateView):
    """Vista base para actualizar contenido."""

    def get_queryset(self):
        # Editors can only edit their own content
        if self.request.user.is_admin():
            return super().get_queryset()
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _("Contenido actualizado exitosamente."))
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ArticleUpdateView(ContentUpdateView):
    """Actualizar artículo."""

    model = Article
    form_class = ArticleForm
    template_name = "content/article_form.html"


class DevocionalUpdateView(ContentUpdateView):
    """Actualizar devocional."""

    model = Devocional
    form_class = DevocionalForm
    template_name = "content/devocional_form.html"


class EstudioBiblicoUpdateView(ContentUpdateView):
    """Actualizar estudio bíblico."""

    model = EstudioBiblico
    form_class = EstudioBiblicoForm
    template_name = "content/estudio_form.html"


class BlogPostUpdateView(ContentUpdateView):
    """Actualizar entrada de blog."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "content/blog_form.html"


class ContentDeleteView(EditorRequiredMixin, DeleteView):
    """Vista base para eliminar contenido."""

    def get_queryset(self):
        # Editors can only delete their own content
        if self.request.user.is_admin():
            return super().get_queryset()
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, _("Contenido eliminado exitosamente."))
        return reverse(f"content:{self.model.__name__.lower()}_list")


class ArticleDeleteView(ContentDeleteView):
    """Eliminar artículo."""

    model = Article
    template_name = "content/article_confirm_delete.html"
    success_url = reverse_lazy("content:article_list")


class DevocionalDeleteView(ContentDeleteView):
    """Eliminar devocional."""

    model = Devocional
    template_name = "content/devocional_confirm_delete.html"
    success_url = reverse_lazy("content:devocional_list")


class EstudioBiblicoDeleteView(ContentDeleteView):
    """Eliminar estudio bíblico."""

    model = EstudioBiblico
    template_name = "content/estudio_confirm_delete.html"
    success_url = reverse_lazy("content:estudio_list")


class BlogPostDeleteView(ContentDeleteView):
    """Eliminar entrada de blog."""

    model = BlogPost
    template_name = "content/blog_confirm_delete.html"
    success_url = reverse_lazy("content:blog_list")


# Category Views
class CategoryListView(AdminRequiredMixin, ListView):
    """Lista de categorías."""

    model = Category
    template_name = "content/category_list.html"
    context_object_name = "categories"
    paginate_by = 20


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Crear categoría."""

    model = Category
    form_class = CategoryForm
    template_name = "content/category_form.html"
    success_url = reverse_lazy("content:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Nueva categoría")
        return context


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Actualizar categoría."""

    model = Category
    form_class = CategoryForm
    template_name = "content/category_form.html"
    success_url = reverse_lazy("content:category_list")


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Eliminar categoría."""

    model = Category
    template_name = "content/category_confirm_delete.html"
    success_url = reverse_lazy("content:category_list")


# Content Publishing Views
class SubmitForReviewView(EditorRequiredMixin, View):
    """Enviar contenido a revisión."""

    def post(self, request, *args, **kwargs):
        content_type = self.kwargs.get("content_type")
        pk = self.kwargs.get("pk")

        # Get the content model
        model_map = {
            "article": Article,
            "devocional": Devocional,
            "estudio": EstudioBiblico,
            "blog": BlogPost,
        }
        model = model_map.get(content_type)
        if not model:
            messages.error(request, _("Tipo de contenido no válido."))
            return redirect("content:article_list")

        obj = get_object_or_404(model, pk=pk, author=request.user)
        obj.status = ContentStatus.IN_REVIEW
        obj.save(update_fields=["status"])

        messages.success(request, _("Contenido enviado a revisión."))
        return redirect(obj.get_absolute_url())


class PublishContentView(AdminRequiredMixin, View):
    """Publicar contenido directamente (solo admin)."""

    def post(self, request, *args, **kwargs):
        content_type = self.kwargs.get("content_type")
        pk = self.kwargs.get("pk")

        model_map = {
            "article": Article,
            "devocional": Devocional,
            "estudio": EstudioBiblico,
            "blog": BlogPost,
        }
        model = model_map.get(content_type)
        if not model:
            messages.error(request, _("Tipo de contenido no válido."))
            return redirect("content:article_list")

        obj = get_object_or_404(model, pk=pk)
        obj.status = ContentStatus.PUBLISHED
        obj.published_at = timezone.now()
        obj.save(update_fields=["status", "published_at"])

        messages.success(request, _("Contenido publicado exitosamente."))
        return redirect(obj.get_absolute_url())


class DashboardView(EditorRequiredMixin, TemplateView):
    """Dashboard del editor."""

    template_name = "content/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get content counts
        base_queryset = (
            Article.objects.all()
            | Devocional.objects.all()
            | EstudioBiblico.objects.all()
            | BlogPost.objects.all()
        )

        if not user.is_admin():
            base_queryset = base_queryset.filter(author=user)

        context["total_content"] = base_queryset.count()
        context["draft_count"] = base_queryset.filter(
            status=ContentStatus.DRAFT
        ).count()
        context["in_review_count"] = base_queryset.filter(
            status=ContentStatus.IN_REVIEW
        ).count()
        context["published_count"] = base_queryset.filter(
            status=ContentStatus.PUBLISHED
        ).count()

        # Recent content
        context["recent_articles"] = Article.objects.all()[:5]
        context["recent_devocionales"] = Devocional.objects.all()[:5]

        context["page_title"] = _("Dashboard de contenido")
        return context
