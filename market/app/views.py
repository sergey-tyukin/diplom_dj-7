import json
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from .models import ProductCategory, Product, Article, User, ProductInCart, Order, ProductInOrder
from .auxiliary_functions import get_cart_by_user


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
    product_slug = request.POST.get('product_name')
    user = request.user

    # Authenticated user
    if request.user.is_authenticated:
        if product_slug:
            product = Product.objects.get(slug=product_slug)
            try:
                product_in_cart = ProductInCart.objects.get(user=user, product=product)
            except ProductInCart.DoesNotExist:
                ProductInCart.objects.create(user=user,
                                             product=product,
                                             count=1)
            else:
                product_in_cart.count += 1
                product_in_cart.save()

        context['cart_list'] = get_cart_by_user(user)

        response = render(request, template, context)
        response.delete_cookie('cart_list')

    # Anonymous user
    else:
        cart_list_str = request.COOKIES.get('cart_list')
        cart_list = json.loads(cart_list_str) if cart_list_str else {}

        if product_slug:
            cart_list[product_slug] = cart_list.get(product_slug, 0) + 1

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

    email = request.POST.get('email').strip()
    password = request.POST.get('password')

    if not User.objects.filter(email=email).exists():
        context['error'] = 'Такого пользователя не существует'
    else:
        user = authenticate(request, username=User.objects.get(email=email), password=password)
        if user:
            login(request, user)

            cart_list_str = request.COOKIES.get('cart_list')
            cart_list = json.loads(cart_list_str) if cart_list_str else {}

            for item, count in cart_list.items():
                try:
                    product_in_cart = ProductInCart.objects.get(product__slug=item)
                except ProductInCart.DoesNotExist:
                    ProductInCart.objects.create(user=user,
                                                 product=Product.objects.get(slug=item),
                                                 count=count)
                else:
                    product_in_cart.count += count
                    product_in_cart.save()

            context['cart_list'] = []
            for item, count in cart_list.items():
                context['cart_list'].append((Product.objects.get(slug=item), count))

            return redirect(index_view)
        context['error'] = 'Пароль неверен'

    return render(request, template, context)


@login_required()
def checkout_view(request):
    user = request.user

    items = ProductInCart.objects.filter(user=user)
    order = Order.objects.create(user=user)
    for item in items:
        ProductInOrder.objects.create(order=order,
                                      product=item.product,
                                      count=item.count)

    ProductInCart.objects.filter(user=user).delete()

    messages.success(request, 'Ваш заказ оформлен')
    return redirect('cart')
