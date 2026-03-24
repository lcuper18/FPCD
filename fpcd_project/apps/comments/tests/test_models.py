"""
Tests para los modelos de comentarios.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.content.models import Article, ContentStatus
from apps.comments.models import Comment, CommentVote, CommentStatus

User = get_user_model()


class CommentModelTest(TestCase):
    """Tests para el modelo Comment."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="comment_author@fpcd.com",
            password="testpass123",
            role="editor",
        )
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article-comment",
            content="Content for testing",
            author=self.user,
            status=ContentStatus.PUBLISHED,
        )

    def test_create_comment(self):
        """Test creación de comentario."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="This is a test comment",
            status=CommentStatus.APPROVED,
            is_approved=True,
        )
        self.assertEqual(comment.content, "This is a test comment")
        self.assertEqual(comment.author, self.user)

    def test_comment_str(self):
        """Test __str__ de comentario."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Test comment",
        )
        self.assertIn("Article#", str(comment))

    def test_get_author_name(self):
        """Test get_author_name."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Test comment",
        )
        self.assertEqual(comment.get_author_name(), "comment_author")

    def test_get_replies(self):
        """Test get_replies."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Parent comment",
            is_approved=True,
        )
        Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Reply comment",
            parent=comment,
            is_approved=True,
        )
        replies = comment.get_replies()
        self.assertEqual(replies.count(), 1)

    def test_has_replies(self):
        """Test has_replies."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Parent comment",
            is_approved=True,
        )
        self.assertFalse(comment.has_replies())

        Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Reply comment",
            parent=comment,
            is_approved=True,
        )
        self.assertTrue(comment.has_replies())

    def test_get_status_class(self):
        """Test get_status_class."""
        comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Test comment",
            status=CommentStatus.APPROVED,
        )
        self.assertEqual(comment.get_status_class(), "green")


class CommentVoteModelTest(TestCase):
    """Tests para el modelo CommentVote."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="voter@fpcd.com",
            password="testpass123",
        )
        self.article = Article.objects.create(
            title="Vote Test Article",
            slug="vote-test-article",
            content="Content",
            author=self.user,
        )
        self.comment = Comment.objects.create(
            content_type="Article",
            content_id=self.article.pk,
            author=self.user,
            content="Test comment",
        )

    def test_create_vote(self):
        """Test creación de voto."""
        vote = CommentVote.objects.create(
            comment=self.comment,
            user=self.user,
            vote_type="up",
        )
        self.assertEqual(vote.vote_type, "up")
        self.assertEqual(vote.comment, self.comment)

    def test_vote_str(self):
        """Test __str__ de voto."""
        vote = CommentVote.objects.create(
            comment=self.comment,
            user=self.user,
            vote_type="up",
        )
        self.assertIn("up", str(vote))
