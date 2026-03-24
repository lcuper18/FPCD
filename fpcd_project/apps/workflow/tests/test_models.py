"""
Tests para los modelos de workflow.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.content.models import Article, ContentStatus
from apps.workflow.models import (
    Review,
    Notification,
    ContentSubmission,
    ReviewStatus,
    NotificationType,
)

User = get_user_model()


class ReviewModelTest(TestCase):
    """Tests para el modelo Review."""

    def setUp(self):
        self.author = User.objects.create_user(
            email="author@fpcd.com",
            password="testpass123",
            role="editor",
        )
        self.reviewer = User.objects.create_user(
            email="reviewer@fpcd.com",
            password="testpass123",
            role="reviewer",
        )
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            content="Content",
            author=self.author,
        )

    def test_create_review(self):
        """Test creación de revisión."""
        review = Review.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            reviewer=self.reviewer,
            author=self.author,
            status=ReviewStatus.PENDING,
        )
        self.assertEqual(review.status, ReviewStatus.PENDING)
        self.assertEqual(review.reviewer, self.reviewer)

    def test_review_str(self):
        """Test __str__ de revisión."""
        review = Review.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            reviewer=self.reviewer,
            author=self.author,
        )
        self.assertIn("Article", str(review))


class NotificationModelTest(TestCase):
    """Tests para el modelo Notification."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@fpcd.com",
            password="testpass123",
        )

    def test_create_notification(self):
        """Test creación de notificación."""
        notification = Notification.objects.create(
            user=self.user,
            notification_type=NotificationType.CONTENT_SUBMITTED,
            title="Test Notification",
            message="Test message",
        )
        self.assertEqual(
            notification.notification_type, NotificationType.CONTENT_SUBMITTED
        )
        self.assertFalse(notification.is_read)

    def test_notification_str(self):
        """Test __str__ de notificación."""
        notification = Notification.objects.create(
            user=self.user,
            notification_type=NotificationType.SYSTEM,
            title="System Notification",
            message="Message",
        )
        self.assertIn(self.user.email, str(notification))


class ContentSubmissionModelTest(TestCase):
    """Tests para el modelo ContentSubmission."""

    def setUp(self):
        self.author = User.objects.create_user(
            email="author@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_submission(self):
        """Test creación de envío."""
        submission = ContentSubmission.objects.create(
            content_type="Article",
            content_id=1,
            author=self.author,
        )
        self.assertEqual(submission.author, self.author)
        self.assertIsNone(submission.reviewed_at)

    def test_submission_str(self):
        """Test __str__ de envío."""
        submission = ContentSubmission.objects.create(
            content_type="Article",
            content_id=1,
            author=self.author,
        )
        self.assertIn("Article", str(submission))
