from django.db import models
from pytils.translit import slugify


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL,
                               blank=True, null=True, related_name='subcategories')
    slug = models.SlugField(max_length=64, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    picture_path = models.CharField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='product')
    slug = models.SlugField(max_length=64, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
