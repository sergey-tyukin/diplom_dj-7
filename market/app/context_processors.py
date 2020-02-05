from .models import ProductCategory


def category(request):
    return {'categories': ProductCategory.objects.prefetch_related('subcategories').filter(parent__isnull=True).order_by('name')}
