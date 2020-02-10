from django import template

register = template.Library()


@register.filter(name='mul')
def mul(char: str, count: int):
    return char * count
