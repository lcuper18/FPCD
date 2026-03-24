"""
URLs para analytics.
"""

from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.DashboardStatsView.as_view(), name="dashboard"),
    path(
        "content/<str:content_type>/<int:pk>/",
        views.analytics_content_detail,
        name="content_detail",
    ),
]
