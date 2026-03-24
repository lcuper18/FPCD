"""
URLs públicas para el portal.
"""

from django.urls import path
from . import views_public

app_name = "public"

urlpatterns = [
    # Home - map both 'home' and 'public:home'
    path("", views_public.HomeView.as_view(), name="home"),
    path("", views_public.HomeView.as_view(), name="public_home"),
    # Articles
    path("articulos/", views_public.ArticleListView.as_view(), name="article_list"),
    path(
        "articulos/<slug:slug>/",
        views_public.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    # Devocionales
    path(
        "devocionales/",
        views_public.DevocionalListView.as_view(),
        name="devocional_list",
    ),
    path(
        "devocionales/<slug:slug>/",
        views_public.DevocionalDetailView.as_view(),
        name="devocional_detail",
    ),
    # Estudios
    path("estudios/", views_public.EstudioListView.as_view(), name="estudio_list"),
    path(
        "estudios/<slug:slug>/",
        views_public.EstudioDetailView.as_view(),
        name="estudio_detail",
    ),
    # Blog
    path("blog/", views_public.BlogListView.as_view(), name="blog_list"),
    path(
        "blog/<slug:slug>/", views_public.BlogDetailView.as_view(), name="blog_detail"
    ),
    # Categories
    path("categorias/", views_public.CategoryListView.as_view(), name="category_list"),
    path(
        "categorias/<slug:slug>/",
        views_public.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    # Search
    path("buscar/", views_public.SearchView.as_view(), name="search"),
    # Pages
    path("sobre-nosotros/", views_public.AboutView.as_view(), name="about"),
    path("contacto/", views_public.ContactView.as_view(), name="contact"),
]
