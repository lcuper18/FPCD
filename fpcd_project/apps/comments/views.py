"""
Vistas para el sistema de comentarios.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings

from apps.content.models import ContentStatus
from .models import Comment, CommentVote, CommentStatus
from .forms import CommentForm, AnonymousCommentForm, ReplyForm


class CommentListView(ListView):
    """Lista de comentarios para un objeto de contenido."""

    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"
    paginate_by = 20

    def get_queryset(self):
        content_type = self.kwargs.get("content_type")
        content_id = self.kwargs.get("content_id")

        return (
            Comment.objects.filter(
                content_type=content_type,
                content_id=content_id,
                parent__isnull=True,  # Only top-level comments
                is_approved=True,
            )
            .select_related("author")
            .prefetch_related("replies", "replies__author")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_type"] = self.kwargs.get("content_type")
        context["content_id"] = self.kwargs.get("content_id")

        # Check if user can post (authenticated or anonymous allowed)
        context["can_comment"] = True

        return context


class CommentCreateView(CreateView):
    """Vista para crear un comentario."""

    model = Comment
    form_class = CommentForm
    template_name = "comments/form.html"

    def get_content_object(self):
        content_type = self.kwargs.get("content_type")
        content_id = self.kwargs.get("content_id")
        from django.apps import apps

        model = apps.get_model("content", content_type)
        return model.objects.get(pk=content_id)

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return CommentForm
        return AnonymousCommentForm

    def form_valid(self, form):
        content_obj = self.get_content_object()

        comment = form.save(commit=False)
        comment.content_type = self.kwargs.get("content_type")
        comment.content_id = self.kwargs.get("content_id")

        if self.request.user.is_authenticated:
            comment.author = self.request.user
        else:
            comment.author_name = form.cleaned_data.get("author_name", "Anónimo")
            comment.author_email = form.cleaned_data.get("author_email", "")

        # Get IP address
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            comment.ip_address = x_forwarded_for.split(",")[0]
        else:
            comment.ip_address = self.request.META.get("REMOTE_ADDR")

        comment.user_agent = self.request.META.get("HTTP_USER_AGENT", "")[:500]

        # Auto-approve if authenticated
        if self.request.user.is_authenticated:
            comment.status = CommentStatus.APPROVED
            comment.is_approved = True

        comment.save()

        messages.success(
            self.request,
            "Comentario publicado exitosamente."
            if comment.is_approved
            else "Tu comentario está pendiente de aprobación.",
        )
        return redirect(comment.get_content_object().get_absolute_url() + "#comments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_obj"] = self.get_content_object()
        return context


class ReplyCreateView(CreateView):
    """Vista para responder a un comentario."""

    model = Comment
    form_class = ReplyForm
    template_name = "comments/form.html"

    def get_parent_comment(self):
        parent_id = self.kwargs.get("parent_id")
        return get_object_or_404(Comment, pk=parent_id)

    def form_valid(self, form):
        parent = self.get_parent_comment()

        comment = form.save(commit=False)
        comment.content_type = parent.content_type
        comment.content_id = parent.content_id
        comment.parent = parent

        if self.request.user.is_authenticated:
            comment.author = self.request.user
            comment.status = CommentStatus.APPROVED
            comment.is_approved = True
        else:
            messages.error(self.request, "Debes estar autenticado para responder.")
            return redirect(parent.get_content_object().get_absolute_url())

        comment.save()

        messages.success(self.request, "Respuesta publicada.")
        return redirect(
            parent.get_content_object().get_absolute_url()
            + "#comment-"
            + str(parent.pk)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_comment"] = self.get_parent_comment()
        return context


class CommentVoteView(LoginRequiredMixin, View):
    """Vista para votar un comentario."""

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        vote_type = request.POST.get("vote_type", "up")

        comment = get_object_or_404(Comment, pk=comment_id)

        # Check if user already voted
        existing_vote = CommentVote.objects.filter(
            comment=comment, user=request.user
        ).first()

        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Remove vote if same
                existing_vote.delete()
                return JsonResponse(
                    {"status": "removed", "votes": comment.votes.count()}
                )
            else:
                # Update vote
                existing_vote.vote_type = vote_type
                existing_vote.save()
                return JsonResponse(
                    {"status": "updated", "votes": comment.votes.count()}
                )
        else:
            # Create new vote
            CommentVote.objects.create(
                comment=comment,
                user=request.user,
                vote_type=vote_type,
            )
            return JsonResponse({"status": "added", "votes": comment.votes.count()})


class CommentApproveView(LoginRequiredMixin, View):
    """Vista para aprobar un comentario."""

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_id)

        # Check permissions
        if not request.user.is_reviewer() and not request.user.is_admin():
            return JsonResponse({"error": "No tienes permiso"}, status=403)

        comment.status = CommentStatus.APPROVED
        comment.is_approved = True
        comment.save()

        return JsonResponse({"status": "approved"})


class CommentRejectView(LoginRequiredMixin, View):
    """Vista para rechazar un comentario."""

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_id)

        if not request.user.is_reviewer() and not request.user.is_admin():
            return JsonResponse({"error": "No tienes permiso"}, status=403)

        comment.status = CommentStatus.REJECTED
        comment.is_approved = False
        comment.save()

        return JsonResponse({"status": "rejected"})


# Template tags helper
def get_comments_count(content_type, content_id):
    """Retorna el número de comentarios aprobados."""
    return Comment.objects.filter(
        content_type=content_type,
        content_id=content_id,
        is_approved=True,
    ).count()
