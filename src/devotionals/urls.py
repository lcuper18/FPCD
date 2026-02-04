from django.urls import path
from . import views

app_name = 'devotionals'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('devocionales/', views.devotional_list_view, name='list'),
    path('devocional/<slug:slug>/', views.devotional_detail_view, name='detail'),
    path('devocional/<slug:slug>/favorito/', views.toggle_favorite_view, name='toggle_favorite'),
    path('mis-favoritos/', views.my_favorites_view, name='my_favorites'),
    path('categoria/<slug:slug>/', views.category_view, name='category'),
    path('buscar/', views.search_view, name='search'),
]
