from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Subscriber
from .forms import SubscriberForm


@require_http_methods(["GET", "POST"])
def subscribe_view(request):
    """Vista de suscripción al newsletter"""
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Verificar si ya está suscrito
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'name': form.cleaned_data['name']}
            )
            
            if created:
                # Si el usuario está autenticado, vincularlo
                if request.user.is_authenticated:
                    subscriber.user = request.user
                    subscriber.save()
                    request.user.subscribed_to_newsletter = True
                    request.user.save()
                
                messages.success(
                    request,
                    '¡Gracias por suscribirte! Recibirás devocionales diarios en tu correo.'
                )
            else:
                if subscriber.is_active:
                    messages.info(request, 'Este correo ya está suscrito a nuestro newsletter.')
                else:
                    # Reactivar suscripción
                    subscriber.is_active = True
                    subscriber.unsubscribed_at = None
                    subscriber.save()
                    messages.success(request, '¡Tu suscripción ha sido reactivada!')
            
            return redirect('devotionals:home')
    else:
        # Prellenar con datos del usuario si está autenticado
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.full_name,
                'email': request.user.email
            }
        form = SubscriberForm(initial=initial_data)
    
    return render(request, 'newsletter/subscribe.html', {'form': form})


def unsubscribe_view(request, email):
    """Vista de cancelación de suscripción"""
    try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.is_active = False
        from django.utils import timezone
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        
        if subscriber.user:
            subscriber.user.subscribed_to_newsletter = False
            subscriber.user.save()
        
        messages.info(request, 'Tu suscripción ha sido cancelada. Esperamos verte pronto.')
    except Subscriber.DoesNotExist:
        messages.error(request, 'No se encontró esta suscripción.')
    
    return redirect('devotionals:home')
