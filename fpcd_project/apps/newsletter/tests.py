"""
Tests para newsletter.
"""

from django.test import TestCase
from django.urls import reverse
from apps.newsletter.models import Subscriber


class SubscriberModelTest(TestCase):
    """Tests para el modelo Subscriber."""

    def test_create_subscriber(self):
        """Test creación de suscriptor."""
        subscriber = Subscriber.objects.create(
            email="test@example.com", first_name="Test"
        )
        self.assertEqual(subscriber.email, "test@example.com")
        self.assertTrue(subscriber.is_active)
        self.assertFalse(subscriber.is_verified)

    def test_subscriber_str(self):
        """Test string representation."""
        subscriber = Subscriber(email="test@example.com")
        self.assertEqual(str(subscriber), "test@example.com")

    def test_subscriber_unique_email(self):
        """Test que el email es único."""
        Subscriber.objects.create(email="unique@example.com")
        with self.assertRaises(Exception):
            Subscriber.objects.create(email="unique@example.com")


class SubscribeViewTest(TestCase):
    """Tests para la vista de suscripción."""

    def test_subscribe_get(self):
        """Test GET request a la página de suscripción."""
        response = self.client.get(reverse("newsletter:subscribe"))
        self.assertEqual(response.status_code, 200)

    def test_subscribe_post_valid(self):
        """Test suscripción con datos válidos."""
        response = self.client.post(
            reverse("newsletter:subscribe"),
            {"email": "new@example.com", "first_name": "John"},
        )
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subscriber.objects.filter(email="new@example.com").exists())

    def test_subscribe_post_invalid(self):
        """Test suscripción con email inválido."""
        response = self.client.post(
            reverse("newsletter:subscribe"), {"email": "invalid-email"}
        )
        self.assertEqual(response.status_code, 200)
        # Should have form errors


class UnsubscribeViewTest(TestCase):
    """Tests para la vista de cancelación."""

    def setUp(self):
        """Crear suscriptor para pruebas."""
        self.subscriber = Subscriber.objects.create(
            email="test@example.com", is_active=True
        )

    def test_unsubscribe_post(self):
        """Test cancelación de suscripción."""
        response = self.client.post(
            reverse("newsletter:unsubscribe"),
            {"email": "test@example.com", "reason": "No quiero más"},
        )
        self.subscriber.refresh_from_db()
        self.assertFalse(self.subscriber.is_active)
