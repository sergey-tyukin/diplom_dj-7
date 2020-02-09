from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser

from pytils.translit import slugify


class User(AbstractUser):
    pass


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
    cart_user = models.ManyToManyField(User, related_name='cart_product',
                                       through='ProductInCart')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Article(models.Model):
    name = models.CharField(max_length=256)
    text = models.CharField(max_length=4096)
    date = models.DateField()
    products = models.ManyToManyField(Product, related_name='article')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-date', 'name']


class ProductInCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_position')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_position')
    count = models.IntegerField()


class Order(models.Model):
    date = models.DateField(default=timezone.now())
    product = models.ManyToManyField(Product, through='ProductInOrder', related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_position')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-date', 'user']


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_position')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_position')
    count = models.IntegerField()
