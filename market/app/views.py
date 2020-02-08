import json
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import ProductCategory, Product, Article, User


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
    template = 'app/cart.html'
    context = {}

    if request.user.is_authenticated:
        response = render(request, template, context)

    else:
        cart_list_str = request.COOKIES.get('cart_list')
        cart_list = json.loads(cart_list_str) if cart_list_str else {}
        product = request.POST.get('product_name')

        if product:
            cart_list[product] = cart_list.get(product, 0) + 1

        context['cart_list'] = []
        for item, count in cart_list.items():
            context['cart_list'].append((Product.objects.get(slug=item), count))

        response = render(request, template, context)
        response.set_cookie('cart_list', json.dumps(cart_list))

    return response


def login_view(request):
    template = 'registration/login.html'
    context = {}
    if request.method == 'GET':
        return render(request, template, context)

    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        context['error'] = 'Такого пользователя не существует'
        return render(request, template, context)
    else:
        user = authenticate(username=user, password=password)
        if user:
            login(request, user)
            return redirect(index_view)
        else:
            context['error'] = 'Пароль неверен'
            return render(request, template, context)



