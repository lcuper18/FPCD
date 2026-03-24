"""
Vistas para el flujo de trabajo.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    View,
    TemplateView,
    RedirectView,
)
from django.urls import reverse_lazy, reverse, get_callable
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

from apps.content.models import ContentStatus
from apps.accounts.permissions import (
    EditorRequiredMixin,
    ReviewerRequiredMixin,
    AdminRequiredMixin,
)
from .models import Review, Notification, ReviewStatus
from .forms import ReviewForm, QuickReviewForm
from .services import ReviewService, NotificationService


class ReviewQueueView(ReviewerRequiredMixin, TemplateView):
    """Vista de cola de revisión para revisores."""

    template_name = "workflow/review_queue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get pending content
        pending = ReviewService.get_pending_reviews(self.request.user)

        context["pending_articles"] = pending.get("articles", [])
        context["pending_devocionales"] = pending.get("devocionales", [])
        context["pending_estudios"] = pending.get("estudios", [])
        context["pending_blog"] = pending.get("blog_posts", [])

        context["page_title"] = "Cola de Revisión"

        return context


class ReviewDetailView(ReviewerRequiredMixin, DetailView):
    """Vista detalle para revisar contenido."""

    template_name = "workflow/review_detail.html"
    context_object_name = "content"

    def get_object(self):
        content_type = self.kwargs.get("content_type")
        content_id = self.kwargs.get("content_id")

        return ReviewService.get_content_for_review(content_type, content_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = self.get_object()

        # Get existing reviews
        reviews = Review.objects.filter(
            content_type=content.__class__.__name__,
            content_id=content.pk,
        ).order_by("-created_at")

        context["reviews"] = reviews
        context["review_form"] = QuickReviewForm()
        context["content_type"] = content.__class__.__name__.lower()

        return context

    def post(self, request, *args, **kwargs):
        content = self.get_object()
        form = QuickReviewForm(request.POST)

        if form.is_valid():
            action = form.cleaned_data["action"]
            comment = form.cleaned_data.get("comment", "")

            if action == "approve":
                ReviewService.approve_content(content, request.user, comment)
                content.status = ContentStatus.PUBLISHED
                content.published_at = timezone.now()
                content.save(update_fields=["status", "published_at"])
                messages.success(request, "Contenido aprobado y publicado.")

            elif action == "reject":
                ReviewService.reject_content(content, request.user, comment)
                messages.warning(request, "Contenido rechazado.")

            elif action == "request_revision":
                ReviewService.request_revision(content, request.user, comment)
                messages.info(request, "Se ha solicitado revisión adicional.")

            return redirect("workflow:review_queue")

        return self.get(request, *args, **kwargs)


class MySubmissionsView(EditorRequiredMixin, ListView):
    """Lista de envíos del editor."""

    model = Review
    template_name = "workflow/my_submissions.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user).order_by("-created_at")


class NotificationListView(LoginRequiredMixin, ListView):
    """Lista de notificaciones del usuario."""

    model = Notification
    template_name = "workflow/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unread_count"] = NotificationService.get_unread_count(
            self.request.user
        )
        context["page_title"] = "Notificaciones"
        return context


class NotificationMarkReadView(LoginRequiredMixin, View):
    """Marca una notificación como leída."""

    def post(self, request, *args, **kwargs):
        notification_id = kwargs.get("pk")
        notification = get_object_or_404(
            Notification, pk=notification_id, user=request.user
        )
        NotificationService.mark_as_read(notification)

        if notification.link:
            return redirect(notification.link)

        return redirect("workflow:notifications")


class NotificationMarkAllReadView(LoginRequiredMixin, View):
    """Marca todas las notificaciones como leídas."""

    def post(self, request, *args, **kwargs):
        NotificationService.mark_all_as_read(request.user)
        messages.success(request, "Todas las notificaciones marcadas como leídas.")
        return redirect("workflow:notifications")


class NotificationCountView(LoginRequiredMixin, View):
    """API endpoint para obtener número de notificaciones no leídas."""

    def get(self, request, *args, **kwargs):
        count = NotificationService.get_unread_count(request.user)
        return JsonResponse({"count": count})


class ReviewHistoryView(LoginRequiredMixin, ListView):
    """Historial de revisiones."""

    model = Review
    template_name = "workflow/review_history.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user

        # For reviewers and admins, show all reviews
        if user.is_reviewer() or user.is_admin():
            return Review.objects.all().order_by("-created_at")

        # For editors, show their reviews
        return Review.objects.filter(author=user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filter options
        context["status_filter"] = self.request.GET.get("status", "")

        return context


class ReviewStatsView(AdminRequiredMixin, TemplateView):
    """Estadísticas de revisión."""

    template_name = "workflow/review_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate stats
        total_reviews = Review.objects.count()
        pending_reviews = Review.objects.filter(status=ReviewStatus.PENDING).count()
        approved_reviews = Review.objects.filter(status=ReviewStatus.APPROVED).count()
        rejected_reviews = Review.objects.filter(status=ReviewStatus.REJECTED).count()

        context["total_reviews"] = total_reviews
        context["pending_reviews"] = pending_reviews
        context["approved_reviews"] = approved_reviews
        context["rejected_reviews"] = rejected_reviews

        # Recent activity
        context["recent_reviews"] = Review.objects.select_related("reviewer", "author")[
            :10
        ]

        context["page_title"] = "Estadísticas de Revisión"

        return context
