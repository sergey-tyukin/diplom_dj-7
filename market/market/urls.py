"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.views import cart_view, empty_secition_view, index_view,\
    login_view, phone_view, smartphones_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='main'),
    path('cart', cart_view, name='cart'),
    path('empty_section.html', empty_secition_view, name='empty_section'),
    path('login.html', login_view, name='login'),
    path('phone.html', phone_view, name='phone'),
    path('smartphones.html', smartphones_view, name='smartphones'),
]
