"""
URLs para la aplicación de comentarios.
"""

from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    # Moderación
    path("moderacion/", views.CommentModerationListView.as_view(), name="moderation"),
    # Reply - must come before <str:content_type>/<int:content_id>/ to avoid shadowing
    path("reply/<int:parent_id>/", views.ReplyCreateView.as_view(), name="reply"),
    # Comment list and create
    path(
        "<str:content_type>/<int:content_id>/",
        views.CommentListView.as_view(),
        name="list",
    ),
    path(
        "<str:content_type>/<int:content_id>/create/",
        views.CommentCreateView.as_view(),
        name="create",
    ),
    # Votes
    path("<int:pk>/vote/", views.CommentVoteView.as_view(), name="vote"),
    # Moderation actions
    path("<int:pk>/approve/", views.CommentApproveView.as_view(), name="approve"),
    path("<int:pk>/reject/", views.CommentRejectView.as_view(), name="reject"),
]
