"""
Vistas para estadísticas y dashboard.
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from apps.analytics.services import AnalyticsService
from apps.content.models import Article, Devocional, EstudioBiblico as Estudio, BlogPost
from apps.workflow.models import Review, ReviewStatus


class DashboardStatsView(LoginRequiredMixin, TemplateView):
    """
    Vista del dashboard de estadísticas.
    """

    template_name = "analytics/dashboard.html"
    login_url = "/accounts/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener parámetros
        days = int(self.request.GET.get("days", 30))

        # Estadísticas generales
        stats = AnalyticsService.get_dashboard_stats(days)

        # Contenido por tipo
        context["total_views"] = stats["total_views"]
        context["unique_visitors"] = stats["unique_visitors"]
        context["views_by_type"] = stats["views_by_type"]
        context["top_content"] = stats["top_content"]
        context["daily_stats"] = stats["daily_stats"]

        # Contenido total
        context["total_articles"] = Article.objects.filter(status="published").count()
        context["total_devocionales"] = Devocional.objects.filter(
            status="published"
        ).count()
        context["total_estudios"] = Estudio.objects.filter(status="published").count()
        context["total_blogs"] = BlogPost.objects.filter(status="published").count()

        # Revisiones pendientes
        context["pending_reviews"] = Review.objects.filter(
            status=ReviewStatus.PENDING
        ).count()

        # Usuarios
        from django.contrib.auth import get_user_model

        User = get_user_model()
        context["total_users"] = User.objects.count()
        context["total_editors"] = User.objects.filter(role="editor").count()
        context["total_reviewers"] = User.objects.filter(role="reviewer").count()

        context["days"] = days
        context["page_title"] = _("Estadísticas")

        return context


@login_required
def analytics_content_detail(request, content_type, pk):
    """
    Vista detallada de estadísticas de un contenido.
    """
    from django.contrib.contenttypes.models import ContentType
    from apps.analytics.models import ContentStats

    # Mapear tipo de contenido
    type_map = {
        "article": ("content.Article", Article),
        "devocional": ("content.Devocional", Devocional),
        "estudio": ("content.Estudio", Estudio),
        "blog": ("content.BlogPost", BlogPost),
    }

    if content_type not in type_map:
        return render(request, "404.html")

    app_label, model_class = type_map[content_type]

    try:
        content_type_obj = ContentType.objects.get(
            app_label=app_label.split(".")[0], model=model_class.__name__.lower()
        )
        content = model_class.objects.get(pk=pk)
        stats = ContentStats.objects.get(content_type=content_type, object_id=pk)
        views_history = AnalyticsService.get_content_views(content, 30)
    except (model_class.DoesNotExist, ContentStats.DoesNotExist):
        return render(request, "404.html")

    return render(
        request,
        "analytics/content_detail.html",
        {
            "content": content,
            "stats": stats,
            "views_history": views_history,
            "page_title": f"Estadísticas: {content.title}",
        },
    )
