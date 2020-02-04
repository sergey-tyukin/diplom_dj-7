from .models import ProductCategory


def category(request):
    return {'categories': ProductCategory.objects.filter(parent__isnull=True).order_by('name')}
