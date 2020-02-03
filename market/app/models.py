from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL,
                               blank=True, null=True, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    picture_path = models.CharField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='product')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
