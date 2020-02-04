from urllib.parse import urlencode

from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse

from .models import ProductCategory, Product


def index_view(request):
    context = {}
    template = 'app/index.html'

    return render(request, template, context)


def category_view(request, category):
    template = 'app/category.html'

    count_per_page = 3
    products = Product.objects.filter(category__slug=category)
    paginator = Paginator(products, count_per_page)

    current_page = int(request.GET.get('page', 1))
    if current_page < 1:
        current_page = 1
    if current_page > paginator.num_pages:
        current_page = paginator.num_pages
    page = paginator.get_page(current_page)

    if page.has_previous():
        prev_page_url = reverse('category', args=[category]) + '?' + \
                        urlencode({'page': page.previous_page_number()})
    else:
        prev_page_url = None

    if page.has_next():
        next_page_url = reverse('category', args=[category]) + '?' + \
                        urlencode({'page': page.next_page_number()})
    else:
        next_page_url = None

    context = {
        'category': ProductCategory.objects.get(slug=category),
        'products': products[(current_page - 1) * count_per_page: current_page * count_per_page],
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url}

    return render(request, template, context)


def product_view(request):
    return render(request, 'app/phone.html', {})


def cart_view(request):
    return render(request, 'app/cart.html', {})


def login_view(request):
    return render(request, 'app/login.html', {})


def phone_view(request):
    return render(request, 'app/phone.html', {})

