from .models import ProductInCart


def get_cart_by_user(user):
    all_products_in_cart = ProductInCart.objects.filter(user=user)

    cart_list = []
    for item in all_products_in_cart:
        cart_list.append((item.product, item.count))

    return cart_list
