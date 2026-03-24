"""
Tests para analytics.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.analytics.models import PageView, DailyStats, ContentStats

User = get_user_model()


class PageViewModelTest(TestCase):
    """Tests para el modelo PageView."""

    def test_page_view_creation(self):
        """Test creación de PageView."""
        user = User.objects.create_user(email="test@example.com", password="test123")
        page_view = PageView.objects.create(
            content_type="article", object_id=1, user=user, ip_address="127.0.0.1"
        )
        self.assertEqual(page_view.content_type, "article")
        self.assertEqual(page_view.object_id, 1)
        self.assertEqual(page_view.user, user)


class DailyStatsModelTest(TestCase):
    """Tests para el modelo DailyStats."""

    def test_daily_stats_creation(self):
        """Test creación de DailyStats."""
        from django.utils import timezone
        from datetime import date

        stats = DailyStats.objects.create(
            date=date.today(), total_views=100, unique_visitors=50
        )
        self.assertEqual(stats.total_views, 100)
        self.assertEqual(stats.unique_visitors, 50)


class ContentStatsModelTest(TestCase):
    """Tests para el modelo ContentStats."""

    def test_content_stats_creation(self):
        """Test creación de ContentStats."""
        stats = ContentStats.objects.create(
            content_type="article", object_id=1, total_views=100, unique_views=50
        )
        self.assertEqual(stats.total_views, 100)
        self.assertEqual(stats.unique_views, 50)


class AnalyticsServiceTest(TestCase):
    """Tests para el servicio de Analytics."""

    def test_get_dashboard_stats(self):
        """Test obtención de estadísticas del dashboard."""
        from apps.analytics.services import AnalyticsService

        stats = AnalyticsService.get_dashboard_stats(days=30)

        self.assertIn("total_views", stats)
        self.assertIn("unique_visitors", stats)
        self.assertIn("views_by_type", stats)
        self.assertIn("top_content", stats)

    def test_get_popular_content(self):
        """Test obtención de contenido popular."""
        from apps.analytics.services import AnalyticsService

        # Create some content stats
        ContentStats.objects.create(
            content_type="article", object_id=1, total_views=100
        )

        popular = AnalyticsService.get_popular_content(content_type="article", limit=10)
        self.assertEqual(len(popular), 1)


class DashboardViewTest(TestCase):
    """Tests para la vista del dashboard."""

    def setUp(self):
        """Crear usuario para pruebas."""
        self.user = User.objects.create_user(
            email="admin@example.com", password="admin123", role="admin"
        )

    def test_dashboard_requires_login(self):
        """Test que el dashboard requiere login."""
        response = self.client.get(reverse("analytics:dashboard"))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        """Test acceso al dashboard con usuario autenticado."""
        self.client.login(email="admin@example.com", password="admin123")
        response = self.client.get(reverse("analytics:dashboard"))
        self.assertEqual(response.status_code, 200)
