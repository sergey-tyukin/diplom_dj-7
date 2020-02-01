from django.shortcuts import render


def cart_view(request):
    return render(request, 'app/cart.html', {})


def empty_secition_view(request):
    return render(request, 'app/empty_section.html', {})


def index_view(request):
    return render(request, 'app/index.html', {})


def login_view(request):
    return render(request, 'app/login.html', {})


def phone_view(request):
    return render(request, 'app/phone.html', {})


def smartphones_view(request):
    return render(request, 'app/smartphones.html', {})
