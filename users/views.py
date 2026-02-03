from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import CustomUser


class RegisterView(CreateView):
    """Vista de registro de usuario"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('devotionals:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '¡Bienvenido a Fe para Cada Día! Tu cuenta ha sido creada exitosamente.')
        return response


class CustomLoginView(LoginView):
    """Vista de inicio de sesión"""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido de nuevo, {form.get_user().full_name}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Vista de cierre de sesión"""
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Has cerrado sesión exitosamente. ¡Que Dios te bendiga!')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    """Dashboard para colaboradores"""
    if not request.user.is_collaborator:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('devotionals:home')
    
    context = {
        'user': request.user,
    }
    return render(request, 'users/dashboard.html', context)
