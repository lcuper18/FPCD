"""
URLs para la aplicación de contenido.
"""

from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Article URLs
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path("articles/create/", views.ArticleCreateView.as_view(), name="article_create"),
    path(
        "articles/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "articles/<slug:slug>/edit/",
        views.ArticleUpdateView.as_view(),
        name="article_update",
    ),
    path(
        "articles/<slug:slug>/delete/",
        views.ArticleDeleteView.as_view(),
        name="article_delete",
    ),
    # Devocional URLs
    path("devocionales/", views.DevocionalListView.as_view(), name="devocional_list"),
    path(
        "devocionales/create/",
        views.DevocionalCreateView.as_view(),
        name="devocional_create",
    ),
    path(
        "devocionales/<slug:slug>/",
        views.DevocionalDetailView.as_view(),
        name="devocional_detail",
    ),
    path(
        "devocionales/<slug:slug>/edit/",
        views.DevocionalUpdateView.as_view(),
        name="devocional_update",
    ),
    path(
        "devocionales/<slug:slug>/delete/",
        views.DevocionalDeleteView.as_view(),
        name="devocional_delete",
    ),
    # Estudio Bíblico URLs
    path("estudios/", views.EstudioBiblicoListView.as_view(), name="estudio_list"),
    path(
        "estudios/create/",
        views.EstudioBiblicoCreateView.as_view(),
        name="estudio_create",
    ),
    path(
        "estudios/<slug:slug>/",
        views.EstudioBiblicoDetailView.as_view(),
        name="estudio_detail",
    ),
    path(
        "estudios/<slug:slug>/edit/",
        views.EstudioBiblicoUpdateView.as_view(),
        name="estudio_update",
    ),
    path(
        "estudios/<slug:slug>/delete/",
        views.EstudioBiblicoDeleteView.as_view(),
        name="estudio_delete",
    ),
    # Blog URLs
    path("blog/", views.BlogPostListView.as_view(), name="blog_list"),
    path("blog/create/", views.BlogPostCreateView.as_view(), name="blog_create"),
    path("blog/<slug:slug>/", views.BlogPostDetailView.as_view(), name="blog_detail"),
    path(
        "blog/<slug:slug>/edit/", views.BlogPostUpdateView.as_view(), name="blog_update"
    ),
    path(
        "blog/<slug:slug>/delete/",
        views.BlogPostDeleteView.as_view(),
        name="blog_delete",
    ),
    # Category URLs
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path(
        "categories/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "categories/<int:pk>/edit/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    # Action URLs
    path(
        "<str:content_type>/<int:pk>/submit/",
        views.SubmitForReviewView.as_view(),
        name="submit_review",
    ),
    path(
        "<str:content_type>/<int:pk>/publish/",
        views.PublishContentView.as_view(),
        name="publish",
    ),
]
