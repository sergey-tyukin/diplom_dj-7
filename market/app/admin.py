from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ProductCategory, Product, Article, User


admin.site.register(User, UserAdmin)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']
    ordering = ['parent', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass