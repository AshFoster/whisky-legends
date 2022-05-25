from django import template

register = template.Library()


@register.filter
def round_down(value):
    if str(value).split('.')[1] == '0':
        return int(value)
    else:
        return value


@register.filter
def calc_subtotal(price, quantity):
    return price * quantity
