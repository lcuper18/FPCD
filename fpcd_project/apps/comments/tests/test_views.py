"""
Tests para las vistas de comentarios.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.content.models import Article, ContentStatus
from apps.comments.models import Comment, CommentStatus

User = get_user_model()


class CommentViewSetupMixin:
    """Mixin con configuración común para tests de comentarios."""

    def setUp(self):
        self.client = Client()
        self.editor = User.objects.create_user(
            email="editor@test.com",
            password="testpass123",
            username="editor",
            role="editor",
        )
        self.reviewer = User.objects.create_user(
            email="reviewer@test.com",
            password="testpass123",
            username="reviewer",
            role="reviewer",
        )
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="testpass123",
            username="admin_user",
            role="admin",
        )
        self.article = Article.objects.create(
            title="Test Article for Comments",
            slug="test-article-comments-views",
            content="Content here",
            author=self.editor,
            status=ContentStatus.PUBLISHED,
        )
        self.approved_comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.editor,
            content="Approved comment content",
            status=CommentStatus.APPROVED,
            is_approved=True,
        )
        self.pending_comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.editor,
            content="Pending comment content",
            status=CommentStatus.PENDING,
            is_approved=False,
        )


class CommentCreateViewTest(CommentViewSetupMixin, TestCase):
    """Tests para CommentCreateView."""

    def test_create_comment_authenticated(self):
        """Usuario autenticado puede crear comentario."""
        self.client.login(email="editor@test.com", password="testpass123")
        url = reverse("comments:create", kwargs={
            "content_type": "Article",
            "content_id": self.article.pk,
        })
        response = self.client.post(url, {"content": "Nuevo comentario de prueba"})
        self.assertEqual(Comment.objects.filter(content="Nuevo comentario de prueba").count(), 1)

    def test_create_comment_auto_approved_for_authenticated(self):
        """Comentarios de usuarios autenticados se aprueban automáticamente."""
        self.client.login(email="editor@test.com", password="testpass123")
        url = reverse("comments:create", kwargs={
            "content_type": "Article",
            "content_id": self.article.pk,
        })
        self.client.post(url, {"content": "Auto-aprobado"})
        comment = Comment.objects.get(content="Auto-aprobado")
        self.assertTrue(comment.is_approved)
        self.assertEqual(comment.status, CommentStatus.APPROVED)


class ReplyCreateViewTest(CommentViewSetupMixin, TestCase):
    """Tests para ReplyCreateView."""

    def test_reply_requires_authentication(self):
        """Responder requiere autenticación."""
        url = reverse("comments:reply", kwargs={"parent_id": self.approved_comment.pk})
        response = self.client.post(url, {"content": "Una respuesta"})
        # Should redirect to login or show error
        self.assertIn(response.status_code, [302, 403])

    def test_reply_creates_child_comment(self):
        """Respuesta crea comentario hijo."""
        self.client.login(email="editor@test.com", password="testpass123")
        url = reverse("comments:reply", kwargs={"parent_id": self.approved_comment.pk})
        self.client.post(url, {"content": "Mi respuesta"})
        reply = Comment.objects.filter(content="Mi respuesta").first()
        self.assertIsNotNone(reply)
        self.assertEqual(reply.parent, self.approved_comment)


class CommentModerationViewTest(CommentViewSetupMixin, TestCase):
    """Tests para CommentModerationListView."""

    def test_moderation_requires_login(self):
        """Moderación requiere autenticación."""
        url = reverse("comments:moderation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_moderation_requires_reviewer_or_admin(self):
        """Moderación requiere rol reviewer o admin."""
        self.client.login(email="editor@test.com", password="testpass123")
        url = reverse("comments:moderation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_reviewer_can_access_moderation(self):
        """Reviewer puede acceder a moderación."""
        self.client.login(email="reviewer@test.com", password="testpass123")
        url = reverse("comments:moderation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context)

    def test_admin_can_access_moderation(self):
        """Admin puede acceder a moderación."""
        self.client.login(email="admin@test.com", password="testpass123")
        url = reverse("comments:moderation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_moderation_filters_by_status(self):
        """Moderación filtra por estado correctamente."""
        self.client.login(email="reviewer@test.com", password="testpass123")
        url = reverse("comments:moderation")
        response = self.client.get(url + "?status=pending")
        comments = list(response.context["comments"])
        for comment in comments:
            self.assertEqual(comment.status, CommentStatus.PENDING)

    def test_moderation_shows_pending_count(self):
        """Dashboard muestra conteo de pendientes."""
        self.client.login(email="reviewer@test.com", password="testpass123")
        url = reverse("comments:moderation")
        response = self.client.get(url)
        self.assertIn("pending_count", response.context)
        self.assertGreaterEqual(response.context["pending_count"], 1)


class CommentApproveRejectViewTest(CommentViewSetupMixin, TestCase):
    """Tests para CommentApproveView y CommentRejectView."""

    def test_approve_requires_permission(self):
        """Aprobar requiere rol adecuado."""
        self.client.login(email="editor@test.com", password="testpass123")
        url = reverse("comments:approve", kwargs={"pk": self.pending_comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_reviewer_can_approve(self):
        """Reviewer puede aprobar comentarios."""
        self.client.login(email="reviewer@test.com", password="testpass123")
        url = reverse("comments:approve", kwargs={"pk": self.pending_comment.pk})
        response = self.client.post(url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.pending_comment.refresh_from_db()
        self.assertTrue(self.pending_comment.is_approved)

    def test_admin_can_reject(self):
        """Admin puede rechazar comentarios."""
        self.client.login(email="admin@test.com", password="testpass123")
        url = reverse("comments:reject", kwargs={"pk": self.approved_comment.pk})
        response = self.client.post(url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.approved_comment.refresh_from_db()
        self.assertEqual(self.approved_comment.status, CommentStatus.REJECTED)
        self.assertFalse(self.approved_comment.is_approved)
