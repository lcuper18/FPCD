"""
URLs para la aplicación de medios.
"""

from django.urls import path
from . import views

app_name = "media_manager"

urlpatterns = [
    # Main
    path("", views.MediaLibraryView.as_view(), name="library"),
    path("upload/", views.MediaUploadView.as_view(), name="upload"),
    path("upload/ajax/", views.MediaUploadAjaxView.as_view(), name="upload_ajax"),
    # File operations
    path("<int:pk>/", views.MediaDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.MediaEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.MediaDeleteView.as_view(), name="delete"),
    path("select/", views.MediaSelectView.as_view(), name="select"),
    # Folders
    path("folders/", views.FolderListView.as_view(), name="folders"),
    path("folders/create/", views.FolderCreateView.as_view(), name="folder_create"),
    path(
        "folders/<int:pk>/delete/",
        views.FolderDeleteView.as_view(),
        name="folder_delete",
    ),
    # API
    path("stats/", views.GetMediaStatsView.as_view(), name="stats"),
]
