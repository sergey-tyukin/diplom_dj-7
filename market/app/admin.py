from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import ProductCategory, Product, Article, User, Order, ProductInOrder


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'user', 'product_count', 'children_display']
    list_filter = ['user']
    search_fields = ['date']

    def children_display(self, obj):
        display_text = f"<a href=http://127.0.0.1:8000/admin/app/productinorder/?order__id__exact={obj.id}>Детали заказа</a>"
        if display_text:
            return mark_safe(display_text)
        return "-"

    def product_count(self, obj):
        return obj.product.count()


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'count']
    list_filter = ['order']
