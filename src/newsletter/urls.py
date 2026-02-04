from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('suscribirse/', views.subscribe_view, name='subscribe'),
    path('cancelar/<str:email>/', views.unsubscribe_view, name='unsubscribe'),
]
