from urllib.parse import urlencode

from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse

from .models import ProductCategory, Product, Article


def index_view(request):
    template = 'app/index.html'

    articles = Article.objects.prefetch_related('products').all()
    context = {'articles': articles}

    return render(request, template, context)


def category_view(request, category_slug):
    template = 'app/category.html'

    count_per_page = 3

    category = ProductCategory.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, count_per_page)

    current_page = int(request.GET.get('page', 1))
    if current_page < 1:
        current_page = 1
    if current_page > paginator.num_pages:
        current_page = paginator.num_pages
    page = paginator.get_page(current_page)

    if page.has_previous():
        prev_page_url = reverse('category', args=[category_slug]) + '?' + \
                        urlencode({'page': page.previous_page_number()})
    else:
        prev_page_url = None

    if page.has_next():
        next_page_url = reverse('category', args=[category_slug]) + '?' + \
                        urlencode({'page': page.next_page_number()})
    else:
        next_page_url = None

    context = {
        'category': category,
        'products': products[(current_page - 1) * count_per_page: current_page * count_per_page],
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url}

    return render(request, template, context)


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    template = 'app/product.html'
    context = {'product': product}

    return render(request, template, context)


def cart_view(request):
    return render(request, 'app/cart.html', {})


def login_view(request):
    return render(request, 'app/login.html', {})


def phone_view(request):
    return render(request, 'app/phone.html', {})

