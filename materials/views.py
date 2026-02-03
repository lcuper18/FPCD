from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Material


def materials_list_view(request):
    """Lista de materiales"""
    materials_list = Material.objects.filter(is_published=True)
    
    # Filtros
    material_type = request.GET.get('type')
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    if material_type:
        materials_list = materials_list.filter(material_type=material_type)
    if category:
        materials_list = materials_list.filter(category__slug=category)
    if search:
        materials_list = materials_list.filter(title__icontains=search)
    
    # Paginación
    paginator = Paginator(materials_list, 12)
    page_number = request.GET.get('page')
    materials = paginator.get_page(page_number)
    
    context = {
        'materials': materials,
        'material_types': Material.TYPE_CHOICES,
    }
    return render(request, 'materials/list.html', context)


def material_detail_view(request, slug):
    """Detalle de un material"""
    material = get_object_or_404(Material, slug=slug, is_published=True)
    material.views += 1
    material.save(update_fields=['views'])
    
    # Materiales relacionados
    related_materials = Material.objects.filter(
        category=material.category,
        is_published=True
    ).exclude(id=material.id)[:3]
    
    context = {
        'material': material,
        'related_materials': related_materials,
    }
    return render(request, 'materials/detail.html', context)
