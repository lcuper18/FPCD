"""
Vistas para la gestión de archivos multimedia.
"""

import os
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.html import format_html
from django.db import models

from apps.accounts.permissions import EditorRequiredMixin, AdminRequiredMixin
from .models import MediaFile, MediaFolder, MediaFileType
from .forms import MediaFileUploadForm, MediaFileEditForm, MediaFolderForm


class MediaLibraryView(EditorRequiredMixin, TemplateView):
    """Vista principal de la biblioteca de medios."""

    template_name = "media_manager/library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get files
        files = MediaFile.objects.filter(is_active=True)

        # Filter by type
        file_type = self.request.GET.get("file_type")
        if file_type:
            files = files.filter(file_type=file_type)

        # Filter by folder
        folder = self.request.GET.get("folder")
        if folder:
            files = files.filter(folder=folder)

        # Search
        search = self.request.GET.get("search")
        if search:
            files = files.filter(
                models.Q(filename__icontains=search)
                | models.Q(title__icontains=search)
                | models.Q(tags__icontains=search)
            )

        # Paginate
        paginator = Paginator(files, 24)
        page = self.request.GET.get("page", 1)
        context["files"] = paginator.get_page(page)

        # Folders
        context["folders"] = MediaFolder.objects.all()

        # Stats
        context["total_images"] = MediaFile.objects.filter(
            file_type=MediaFileType.IMAGE, is_active=True
        ).count()
        context["total_documents"] = MediaFile.objects.filter(
            file_type=MediaFileType.DOCUMENT, is_active=True
        ).count()
        context["total_files"] = MediaFile.objects.filter(is_active=True).count()

        context["page_title"] = "Biblioteca de Medios"
        context["upload_form"] = MediaFileUploadForm()

        return context


class MediaUploadView(EditorRequiredMixin, CreateView):
    """Vista para subir archivos."""

    model = MediaFile
    form_class = MediaFileUploadForm
    template_name = "media_manager/upload.html"
    success_url = reverse_lazy("media_manager:library")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        messages.success(self.request, "Archivo subido exitosamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Subir Archivo"
        return context


class MediaUploadAjaxView(EditorRequiredMixin, View):
    """Vista AJAX para subir archivos."""

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist("files")
        uploaded = []

        for f in files:
            media_file = MediaFile.objects.create(
                file=f,
                filename=f.name,
                uploader=request.user,
            )
            uploaded.append(
                {
                    "id": media_file.id,
                    "name": media_file.filename,
                    "url": media_file.file.url,
                    "type": media_file.file_type,
                    "size": media_file.get_file_size_display(),
                }
            )

        return JsonResponse(
            {
                "success": True,
                "files": uploaded,
            }
        )


class MediaDetailView(EditorRequiredMixin, DetailView):
    """Vista detalle de archivo."""

    model = MediaFile
    template_name = "media_manager/detail.html"
    context_object_name = "file"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.object.filename
        context["edit_form"] = MediaFileEditForm(instance=self.object)
        return context


class MediaEditView(EditorRequiredMixin, UpdateView):
    """Vista para editar metadatos de archivo."""

    model = MediaFile
    form_class = MediaFileEditForm
    template_name = "media_manager/edit.html"
    success_url = reverse_lazy("media_manager:library")

    def form_valid(self, form):
        messages.success(self.request, "Archivo actualizado exitosamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Editar {self.object.filename}"
        return context


class MediaDeleteView(EditorRequiredMixin, DeleteView):
    """Vista para eliminar archivo."""

    model = MediaFile
    template_name = "media_manager/delete.html"
    success_url = reverse_lazy("media_manager:library")

    def form_valid(self, form):
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, "Archivo eliminado exitosamente.")
        return redirect(self.get_success_url())


class MediaSelectView(View):
    """Vista para seleccionar archivos (para usar en modals)."""

    def get(self, request, *args, **kwargs):
        files = MediaFile.objects.filter(is_active=True)

        # Filter by type
        file_type = request.GET.get("type")
        if file_type:
            files = files.filter(file_type=file_type)

        # Search
        search = request.GET.get("search")
        if search:
            files = files.filter(filename__icontains=search)

        files = files[:20]

        return JsonResponse(
            {
                "files": [
                    {
                        "id": f.id,
                        "name": f.filename,
                        "url": f.file.url,
                        "thumbnail": f.thumbnail.url if f.thumbnail else None,
                        "type": f.file_type,
                    }
                    for f in files
                ]
            }
        )


# Folder Views
class FolderListView(AdminRequiredMixin, ListView):
    """Lista de carpetas."""

    model = MediaFolder
    template_name = "media_manager/folder_list.html"
    context_object_name = "folders"


class FolderCreateView(AdminRequiredMixin, CreateView):
    """Crear carpeta."""

    model = MediaFolder
    form_class = MediaFolderForm
    template_name = "media_manager/folder_form.html"
    success_url = reverse_lazy("media_manager:library")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Carpeta creada exitosamente.")
        return super().form_valid(form)


class FolderDeleteView(AdminRequiredMixin, DeleteView):
    """Eliminar carpeta."""

    model = MediaFolder
    template_name = "media_manager/folder_delete.html"
    success_url = reverse_lazy("media_manager:folders")

    def form_valid(self, form):
        # Move files to root
        MediaFile.objects.filter(folder=self.object.name).update(folder="")
        messages.success(self.request, "Carpeta eliminada exitosamente.")
        return redirect(self.get_success_url())


# Utility Views
class GetMediaStatsView(EditorRequiredMixin, View):
    """Obtener estadísticas de medios."""

    def get(self, request, *args, **kwargs):
        stats = {
            "total": MediaFile.objects.filter(is_active=True).count(),
            "images": MediaFile.objects.filter(
                file_type=MediaFileType.IMAGE, is_active=True
            ).count(),
            "documents": MediaFile.objects.filter(
                file_type=MediaFileType.DOCUMENT, is_active=True
            ).count(),
            "videos": MediaFile.objects.filter(
                file_type=MediaFileType.VIDEO, is_active=True
            ).count(),
            "audio": MediaFile.objects.filter(
                file_type=MediaFileType.AUDIO, is_active=True
            ).count(),
            "other": MediaFile.objects.filter(
                file_type=MediaFileType.OTHER, is_active=True
            ).count(),
        }
        return JsonResponse(stats)
