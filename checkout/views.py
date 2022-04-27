from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('shop'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': ('pk_test_51Kaxe2JS0QBw02O9dfhfpAaHPB8eGMssEOGeG'
                              'hYiC359yRU6p8xT96Q2Kv3NMmSV98PErfdQUgjfeHyfzM2'
                              'dpnW0001vV6vbU1'),
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
