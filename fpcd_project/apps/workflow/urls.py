"""
URLs para la aplicación de workflow.
"""

from django.urls import path
from . import views

app_name = "workflow"

urlpatterns = [
    # Review
    path("review/queue/", views.ReviewQueueView.as_view(), name="review_queue"),
    path(
        "review/<str:content_type>/<int:content_id>/",
        views.ReviewDetailView.as_view(),
        name="review_detail",
    ),
    path("review/history/", views.ReviewHistoryView.as_view(), name="review_history"),
    path("review/stats/", views.ReviewStatsView.as_view(), name="review_stats"),
    # Submissions
    path("submissions/", views.MySubmissionsView.as_view(), name="my_submissions"),
    # Notifications
    path("notifications/", views.NotificationListView.as_view(), name="notifications"),
    path(
        "notifications/<int:pk>/read/",
        views.NotificationMarkReadView.as_view(),
        name="notification_read",
    ),
    path(
        "notifications/read-all/",
        views.NotificationMarkAllReadView.as_view(),
        name="notifications_read_all",
    ),
    path(
        "notifications/count/",
        views.NotificationCountView.as_view(),
        name="notification_count",
    ),
]
