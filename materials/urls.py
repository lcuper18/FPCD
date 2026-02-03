from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.materials_list_view, name='list'),
    path('<slug:slug>/', views.material_detail_view, name='detail'),
]
