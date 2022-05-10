# CREDIT - Idea and basic structure of contexts.py came from
# Code Institue's walkthrough project 'Boutique Ado'
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product


def cart_contents(request):
    """
    Calculates and returns cart related context that can
    be used throughout all apps in this project
    """
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    updating_cart = request.session.get('updating_cart', False)
    previous_url = request.META.get('HTTP_REFERER')
    from_login_register = False

    if previous_url:
        if ('accounts/signup/' in previous_url or
                'accounts/login/' in previous_url):
            from_login_register = True

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            total += quantity * product.price
            product_count += quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
            })
        except ObjectDoesNotExist:
            pass

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(
            settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'updating_cart': updating_cart,
        'from_login_register': from_login_register,
    }

    return context
