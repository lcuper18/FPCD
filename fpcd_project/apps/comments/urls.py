"""
URLs para la aplicación de comentarios.
"""

from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    # Comment operations
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
    path("reply/<int:parent_id>/", views.ReplyCreateView.as_view(), name="reply"),
    # Votes
    path("<int:pk>/vote/", views.CommentVoteView.as_view(), name="vote"),
    # Moderation
    path("<int:pk>/approve/", views.CommentApproveView.as_view(), name="approve"),
    path("<int:pk>/reject/", views.CommentRejectView.as_view(), name="reject"),
]
