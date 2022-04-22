from django import template

register = template.Library()


@register.filter
def round_down(value):
    if str(value).split('.')[1] == '0':
        return int(value)
    else:
        return value


# CREDIT - idea came from Code Institue's walkthrough project 'Boutique Ado'
@register.filter
def calc_subtotal(price, quantity):
    return price * quantity
