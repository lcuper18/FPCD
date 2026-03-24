"""
Servicios para tracking y estadísticas de analytics.
"""

from django.db.models import Count, Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from .models import PageView, DailyStats, ContentStats
from apps.content.models import Article, Devocional, EstudioBiblico as Estudio, BlogPost


class AnalyticsService:
    """
    Servicio para gestionar analíticas y estadísticas.
    """

    @staticmethod
    def track_page_view(request, content_object):
        """
        Registra una vista de página.
        """
        # Determinar tipo de contenido y modelo
        content_type_str = "article"
        content_type_obj = ContentType.objects.get_for_model(Article)

        if isinstance(content_object, Devocional):
            content_type_str = "devocional"
            content_type_obj = ContentType.objects.get_for_model(Devocional)
        elif isinstance(content_object, Estudio):
            content_type_str = "estudio"
            content_type_obj = ContentType.objects.get_for_model(Estudio)
        elif isinstance(content_object, BlogPost):
            content_type_str = "blog"
            content_type_obj = ContentType.objects.get_for_model(BlogPost)

        # Obtener IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        # Crear registro de vista
        page_view = PageView.objects.create(
            content_type=content_type_str,
            object_id=content_object.pk,
            content_type_obj=content_type_obj,
            content_object=content_object,
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key
            if hasattr(request, "session")
            else None,
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            referrer=request.META.get("HTTP_REFERER", "")[:500],
        )

        # Incrementar contador en el contenido
        content_object.views = F("views") + 1
        content_object.save(update_fields=["views"])

        # Actualizar o crear stats de contenido
        AnalyticsService.update_content_stats(content_object, content_type_str)

        # Actualizar stats diarias
        AnalyticsService.update_daily_stats(content_type_str)

        return page_view

    @staticmethod
    def update_content_stats(content_object, content_type):
        """
        Actualiza las estadísticas de un contenido.
        """
        content_type_obj = ContentType.objects.get_for_model(content_object.__class__)

        stats, created = ContentStats.objects.get_or_create(
            content_type=content_type,
            object_id=content_object.pk,
            defaults={
                "content_type_obj": content_type_obj,
                "content_object": content_object,
                "total_views": 0,
                "unique_views": 0,
            },
        )
        stats.total_views = F("total_views") + 1
        stats.last_viewed = timezone.now()
        stats.save(update_fields=["total_views", "last_viewed"])

    @staticmethod
    def update_daily_stats(content_type):
        """
        Actualiza las estadísticas diarias.
        """
        today = timezone.now().date()

        stats, created = DailyStats.objects.get_or_create(
            date=today,
            defaults={
                "total_views": 0,
                "unique_visitors": 0,
                "article_views": 0,
                "devotional_views": 0,
                "study_views": 0,
                "blog_views": 0,
                "new_subscribers": 0,
            },
        )

        # Incrementar según el tipo
        field_map = {
            "article": "article_views",
            "devocional": "devotional_views",
            "estudio": "study_views",
            "blog": "blog_views",
        }

        field = field_map.get(content_type, "total_views")
        setattr(stats, field, F(field) + 1)
        stats.total_views = F("total_views") + 1
        stats.save(update_fields=[field, "total_views"])

    @staticmethod
    def get_dashboard_stats(days=30):
        """
        Obtiene estadísticas para el dashboard.
        """
        since = timezone.now() - timedelta(days=days)

        # Vistas totales
        total_views = PageView.objects.filter(viewed_at__gte=since).count()

        # Visitantes únicos
        unique_visitors = (
            PageView.objects.filter(viewed_at__gte=since)
            .values("session_key")
            .distinct()
            .count()
        )

        # Vistas por tipo
        views_by_type = (
            PageView.objects.filter(viewed_at__gte=since)
            .values("content_type")
            .annotate(count=Count("id"))
        )

        # Contenido más visto
        top_content = ContentStats.objects.select_related("content_type_obj").order_by(
            "-total_views"
        )[:10]

        # Estadísticas diarias de la última semana
        daily_stats = DailyStats.objects.filter(
            date__gte=timezone.now().date() - timedelta(days=7)
        ).order_by("date")

        return {
            "total_views": total_views,
            "unique_visitors": unique_visitors,
            "views_by_type": {
                item["content_type"]: item["count"] for item in views_by_type
            },
            "top_content": top_content,
            "daily_stats": daily_stats,
        }

    @staticmethod
    def get_content_views(content_object, days=30):
        """
        Obtiene las vistas de un contenido específico.
        """
        since = timezone.now() - timedelta(days=days)

        views = (
            PageView.objects.filter(content_object=content_object, viewed_at__gte=since)
            .annotate(date=TruncDate("viewed_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        return views

    @staticmethod
    def get_popular_content(content_type=None, limit=10):
        """
        Obtiene el contenido más popular.
        """
        queryset = (
            ContentStats.objects.select_related("content_type_obj")
            .filter(total_views__gt=0)
            .order_by("-total_views")
        )

        if content_type:
            queryset = queryset.filter(content_type=content_type)

        return queryset[:limit]

    @staticmethod
    def aggregate_daily_stats():
        """
        Agrega las estadísticas del día anterior.
        """
        yesterday = timezone.now().date() - timedelta(days=1)
        start_of_day = timezone.make_aware(
            timezone.datetime.combine(yesterday, timezone.datetime.min.time())
        )
        end_of_day = start_of_day + timedelta(days=1)

        # Crear o obtener stats del día
        stats, created = DailyStats.objects.get_or_create(
            date=yesterday,
            defaults={},
        )

        # Contar vistas
        total_views = PageView.objects.filter(
            viewed_at__gte=start_of_day, viewed_at__lt=end_of_day
        ).count()

        unique_visitors = (
            PageView.objects.filter(
                viewed_at__gte=start_of_day, viewed_at__lt=end_of_day
            )
            .values("session_key")
            .distinct()
            .count()
        )

        # Actualizar stats
        stats.total_views = total_views
        stats.unique_visitors = unique_visitors
        stats.save(update_fields=["total_views", "unique_visitors"])

        return stats
