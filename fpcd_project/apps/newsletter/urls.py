"""
URLs para newsletter.
"""

from django.urls import path
from . import views

app_name = "newsletter"

urlpatterns = [
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("subscribe/ajax/", views.subscribe_ajax, name="subscribe_ajax"),
    path("unsubscribe/", views.UnsubscribeView.as_view(), name="unsubscribe"),
    path("verify/<str:token>/", views.verify_email, name="verify"),
    path("archive/", views.NewsletterListView.as_view(), name="archive"),
]
