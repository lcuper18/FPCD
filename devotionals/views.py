from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import date
from .models import Devotional, Category, Comment, Favorite


def home_view(request):
    """Página principal con devocional del día"""
    today = date.today()
    
    # Devocional del día
    today_devotional = Devotional.objects.filter(
        publish_date=today,
        status='published'
    ).first()
    
    # Si no hay devocional hoy, mostrar el más reciente
    if not today_devotional:
        today_devotional = Devotional.objects.filter(
            publish_date__lte=today,
            status='published'
        ).first()
    
    # Devocionales recientes
    recent_devotionals = Devotional.objects.filter(
        status='published',
        publish_date__lte=today
    ).exclude(id=today_devotional.id if today_devotional else None)[:6]
    
    # Categorías
    categories = Category.objects.all()[:8]
    
    context = {
        'today_devotional': today_devotional,
        'recent_devotionals': recent_devotionals,
        'categories': categories,
        'today': today,
    }
    return render(request, 'devotionals/home.html', context)


def devotional_list_view(request):
    """Lista de todos los devocionales"""
    devotionals_list = Devotional.objects.filter(
        status='published',
        publish_date__lte=date.today()
    )
    
    # Filtros
    category_slug = request.GET.get('category')
    search = request.GET.get('search')
    tag = request.GET.get('tag')
    
    if category_slug:
        devotionals_list = devotionals_list.filter(category__slug=category_slug)
    if search:
        devotionals_list = devotionals_list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(bible_reference__icontains=search)
        )
    if tag:
        devotionals_list = devotionals_list.filter(tags__icontains=tag)
    
    # Paginación
    paginator = Paginator(devotionals_list, 12)
    page_number = request.GET.get('page')
    devotionals = paginator.get_page(page_number)
    
    context = {
        'devotionals': devotionals,
        'categories': Category.objects.all(),
    }
    return render(request, 'devotionals/list.html', context)


def devotional_detail_view(request, slug):
    """Detalle de un devocional"""
    devotional = get_object_or_404(
        Devotional,
        slug=slug,
        status='published',
        publish_date__lte=date.today()
    )
    
    # Incrementar vistas
    devotional.increment_views()
    
    # Comentarios aprobados
    comments = devotional.comments.filter(is_approved=True)
    
    # Verificar si es favorito del usuario
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            devotional=devotional
        ).exists()
    
    # Devocionales relacionados
    related_devotionals = Devotional.objects.filter(
        category=devotional.category,
        status='published'
    ).exclude(id=devotional.id)[:3]
    
    # Manejar nuevo comentario
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                devotional=devotional,
                user=request.user,
                content=content
            )
            messages.success(request, 'Tu comentario ha sido enviado y será revisado pronto.')
            return redirect('devotionals:detail', slug=slug)
    
    context = {
        'devotional': devotional,
        'comments': comments,
        'is_favorite': is_favorite,
        'related_devotionals': related_devotionals,
    }
    return render(request, 'devotionals/detail.html', context)


@login_required
def toggle_favorite_view(request, slug):
    """Agregar/quitar de favoritos"""
    devotional = get_object_or_404(Devotional, slug=slug)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        devotional=devotional
    )
    
    if not created:
        favorite.delete()
        messages.info(request, 'Devocional removido de favoritos.')
    else:
        messages.success(request, 'Devocional agregado a favoritos.')
    
    return redirect('devotionals:detail', slug=slug)


@login_required
def my_favorites_view(request):
    """Devocionales favoritos del usuario"""
    favorites = Favorite.objects.filter(user=request.user).select_related('devotional')
    
    context = {
        'favorites': favorites,
    }
    return render(request, 'devotionals/favorites.html', context)


def category_view(request, slug):
    """Devocionales por categoría"""
    category = get_object_or_404(Category, slug=slug)
    devotionals = Devotional.objects.filter(
        category=category,
        status='published',
        publish_date__lte=date.today()
    )
    
    paginator = Paginator(devotionals, 12)
    page_number = request.GET.get('page')
    devotionals_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'devotionals': devotionals_page,
    }
    return render(request, 'devotionals/category.html', context)


def search_view(request):
    """Búsqueda de devocionales"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Devotional.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(bible_reference__icontains=query) |
            Q(tags__icontains=query),
            status='published',
            publish_date__lte=date.today()
        )
    
    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    results_page = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'results': results_page,
    }
    return render(request, 'devotionals/search.html', context)
