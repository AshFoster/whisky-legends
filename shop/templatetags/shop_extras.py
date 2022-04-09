from django import template

register = template.Library()


# CREDIT - https://code.djangoproject.com/ticket/12486
@register.filter
def lookup(dic, key):
    return dic[key]
