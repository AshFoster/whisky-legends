from django import template

register = template.Library()


# CREDIT - https://code.djangoproject.com/ticket/12486
@register.filter
def lookup(dic, key):
    return dic[key]


# CREDIT - https://stackoverflow.com/questions/9948095/variable-subtraction-in-django-templates
@register.filter
def subtract(value, arg):
    return value - arg


# CREDIT - https://stackoverflow.com/questions/63662873/check-variable-is-numerical-django-template
@register.filter()
def is_numeric(value):
    return str(value).isnumeric()