"""
Vistas para newsletter y suscripciones.
"""

from django.views.generic import FormView, TemplateView, View
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import Subscriber, Newsletter, NewsletterArchive
from .forms import SubscribeForm, UnsubscribeForm
import secrets


class SubscribeView(FormView):
    """
    Vista para suscribirse al newsletter.
    """

    form_class = SubscribeForm
    template_name = "newsletter/subscribe.html"
    success_url = "/"

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        first_name = form.cleaned_data.get("first_name", "")

        # Crear o actualizar suscriptor
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "is_active": True,
                "verification_token": secrets.token_urlsafe(32),
            },
        )

        if not created:
            if subscriber.is_active:
                messages.info(
                    self.request, _("Ya estás suscrito a nuestro newsletter.")
                )
            else:
                # Reactivar suscripción
                subscriber.is_active = True
                subscriber.unsubscribed_at = None
                subscriber.save()
                messages.success(self.request, _("Tu suscripción ha sido reactivada."))
        else:
            messages.success(
                self.request,
                _("¡Te has suscrito exitosamente! Revisa tu correo para confirmar."),
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        # Para AJAX
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = str(error_list[0])
            return JsonResponse({"success": False, "errors": errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Suscribirse al newsletter")
        return context


@require_http_methods(["POST"])
def subscribe_ajax(request):
    """
    Vista AJAX para suscripción rápida.
    """
    form = SubscribeForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data["email"].lower()
        first_name = form.cleaned_data.get("first_name", "")

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "is_active": True,
                "verification_token": secrets.token_urlsafe(32),
            },
        )

        if not created and subscriber.is_active:
            return JsonResponse(
                {"success": False, "message": _("Ya estás suscrito al newsletter.")},
                status=400,
            )

        return JsonResponse(
            {"success": True, "message": _("¡Te has suscrito exitosamente!")}
        )

    return JsonResponse({"success": False, "errors": form.errors}, status=400)


class UnsubscribeView(FormView):
    """
    Vista para cancelar suscripción.
    """

    form_class = UnsubscribeForm
    template_name = "newsletter/unsubscribe.html"
    success_url = "/"

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        reason = form.cleaned_data.get("reason", "")

        try:
            subscriber = Subscriber.objects.get(email__iexact=email)
            subscriber.is_active = False
            subscriber.unsubscribed_reason = reason
            from django.utils import timezone

            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()

            messages.success(
                self.request,
                _(
                    "Tu suscripción ha sido cancelada. ¡ Esperamos verte de vuelta pronto !"
                ),
            )
        except Subscriber.DoesNotExist:
            messages.error(
                self.request, _("Este correo no está suscrito a nuestro newsletter.")
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Cancelar suscripción")
        return context


class NewsletterListView(TemplateView):
    """
    Lista de boletines enviados (archivados).
    """

    template_name = "newsletter/archive.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newsletters"] = NewsletterArchive.objects.all()[:20]
        context["page_title"] = _("Boletines anteriores")
        return context


def verify_email(request, token):
    """
    Vista para verificar email.
    """
    try:
        subscriber = Subscriber.objects.get(verification_token=token)
        subscriber.is_verified = True
        subscriber.verification_token = ""
        subscriber.save()

        messages.success(request, _("Tu correo ha sido verificado correctamente."))
    except Subscriber.DoesNotExist:
        messages.error(request, _("Token de verificación inválido."))

    return redirect("home")
