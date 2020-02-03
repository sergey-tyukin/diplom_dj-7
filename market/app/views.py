from django.shortcuts import render

from .models import ProductCategory, Product


def get_menu_items():
    return ProductCategory.objects.filter(parent__isnull=True)


def cart_view(request):
    return render(request, 'app/cart.html', {})


def empty_secition_view(request):
    context = {'categories': get_menu_items()}
    template = 'app/empty_section.html'

    return render(request, template, context)


def index_view(request):
    context = {'categories': get_menu_items()}
    template = 'app/index.html'

    return render(request, template, context)


def login_view(request):
    return render(request, 'app/login.html', {})


def phone_view(request):
    return render(request, 'app/phone.html', {})


def smartphones_view(request):
    context = {'categories': get_menu_items()}
    template = 'app/smartphones.html'

    return render(request, template, context)

