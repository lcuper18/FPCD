"""
Servicios para el flujo de trabajo.
"""

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.content.models import ContentStatus
from .models import (
    Review,
    ReviewStatus,
    Notification,
    NotificationType,
    ContentSubmission,
)

User = get_user_model()


class ReviewService:
    """Servicio para gestionar revisiones de contenido."""

    @staticmethod
    def submit_for_review(content, author, notes=""):
        """
        Envía contenido para revisión.
        """
        # Create submission record
        submission = ContentSubmission.objects.create(
            content_type=content.__class__.__name__,
            content_id=content.pk,
            author=author,
            notes=notes,
        )

        # Notify reviewers
        reviewers = User.objects.filter(role="reviewer") | User.objects.filter(
            role="admin"
        )
        for reviewer in reviewers.distinct():
            NotificationService.create_notification(
                user=reviewer,
                notification_type=NotificationType.CONTENT_SUBMITTED,
                title=f"Nuevo contenido para revisión",
                message=f"{author.get_full_name() or author.email} ha enviado '{content.title}' para revisión.",
                link=f"/content/review/{content.__class__.__name__.lower()}/{content.pk}/",
            )

        # Update content status
        content.status = ContentStatus.IN_REVIEW
        content.save(update_fields=["status"])

        return submission

    @staticmethod
    def create_review(content, reviewer, status, comment="", feedback=""):
        """
        Crea una revisión de contenido.
        """
        review = Review.objects.create(
            content_type=content.__class__.__name__,
            content_id=content.pk,
            reviewer=reviewer,
            author=content.author,
            status=status,
            comment=comment,
            feedback=feedback,
        )

        # Update submission
        ContentSubmission.objects.filter(
            content_type=content.__class__.__name__,
            content_id=content.pk,
        ).update(reviewed_at=timezone.now())

        # Notify author
        notification_type_map = {
            ReviewStatus.APPROVED: NotificationType.CONTENT_APPROVED,
            ReviewStatus.REJECTED: NotificationType.CONTENT_REJECTED,
            ReviewStatus.REVISION_REQUIRED: NotificationType.CONTENT_REJECTED,
        }

        notification_type = notification_type_map.get(status, NotificationType.SYSTEM)
        title_map = {
            ReviewStatus.APPROVED: "Contenido aprobado",
            ReviewStatus.REJECTED: "Contenido rechazado",
            ReviewStatus.REVISION_REQUIRED: "Se requiere revisión",
        }

        title = title_map.get(status, "Actualización de contenido")

        NotificationService.create_notification(
            user=content.author,
            notification_type=notification_type,
            title=title,
            message=f"Tu contenido '{content.title}' ha sido {status.replace('_', ' ')}.",
            link=f"/content/{content.__class__.__name__.lower()}/{content.slug}/",
        )

        return review

    @staticmethod
    def approve_content(content, reviewer, comment=""):
        """Aprueba contenido."""
        return ReviewService.create_review(
            content=content,
            reviewer=reviewer,
            status=ReviewStatus.APPROVED,
            comment=comment,
        )

    @staticmethod
    def reject_content(content, reviewer, comment="", feedback=""):
        """Rechaza contenido."""
        # Update content status
        content.status = ContentStatus.REJECTED
        content.save(update_fields=["status"])

        return ReviewService.create_review(
            content=content,
            reviewer=reviewer,
            status=ReviewStatus.REJECTED,
            comment=comment,
            feedback=feedback,
        )

    @staticmethod
    def request_revision(content, reviewer, comment="", feedback=""):
        """Solicita revisión adicional."""
        # Update content status back to draft
        content.status = ContentStatus.DRAFT
        content.save(update_fields=["status"])

        return ReviewService.create_review(
            content=content,
            reviewer=reviewer,
            status=ReviewStatus.REVISION_REQUIRED,
            comment=comment,
            feedback=feedback,
        )


class NotificationService:
    """Servicio para gestionar notificaciones."""

    @staticmethod
    def create_notification(user, notification_type, title, message, link=""):
        """
        Crea una notificación para un usuario.
        """
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
        )

    @staticmethod
    def get_unread_count(user):
        """Obtiene el número de notificaciones no leídas."""
        return Notification.objects.filter(user=user, is_read=False).count()

    @staticmethod
    def get_notifications(user, include_read=False, limit=20):
        """
        Obtiene las notificaciones de un usuario.
        """
        queryset = Notification.objects.filter(user=user)
        if not include_read:
            queryset = queryset.filter(is_read=False)
        return queryset[:limit]

    @staticmethod
    def mark_as_read(notification):
        """Marca una notificación como leída."""
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=["is_read", "read_at"])

    @staticmethod
    def mark_all_as_read(user):
        """Marca todas las notificaciones como leídas."""
        Notification.objects.filter(user=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now(),
        )

    @staticmethod
    def delete_old_notifications(days=30):
        """Elimina notificaciones antiguas."""
        from django.utils import timezone
        from datetime import timedelta

        cutoff_date = timezone.now() - timedelta(days=days)
        Notification.objects.filter(
            created_at__lt=cutoff_date,
            is_read=True,
        ).delete()


class ContentService:
    """Servicio para operaciones de contenido."""

    @staticmethod
    def get_pending_reviews(user):
        """
        Obtiene contenido pendiente de revisión para un revisor.
        """
        if user.is_admin():
            # Admin can review everything
            return {
                "articles": ContentService._get_pending_type("Article"),
                "devocionales": ContentService._get_pending_type("Devocional"),
                "estudios": ContentService._get_pending_type("EstudioBiblico"),
                "blog_posts": ContentService._get_pending_type("BlogPost"),
            }
        elif user.is_reviewer():
            return {
                "articles": ContentService._get_pending_type("Article"),
                "devocionales": ContentService._get_pending_type("Devocional"),
                "estudios": ContentService._get_pending_type("EstudioBiblico"),
                "blog_posts": ContentService._get_pending_type("BlogPost"),
            }
        return {}

    @staticmethod
    def _get_pending_type(model_name):
        """Obtiene contenido pendiente de un tipo específico."""
        from django.apps import apps

        model = apps.get_model("content", model_name)
        return model.objects.filter(status=ContentStatus.IN_REVIEW)

    @staticmethod
    def get_content_for_review(content_type, content_id):
        """Obtiene el objeto de contenido para revisión."""
        from django.apps import apps

        model = apps.get_model("content", content_type)
        return model.objects.get(pk=content_id)
