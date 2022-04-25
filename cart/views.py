from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from shop.models import Product


def view_cart(request):
    """ A view to return the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """
    A view to add a chosen quantity of a specified
    product to the cart
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(
            request,
            f'Updated "{product.brand.friendly_name}: '
            f'{product.name}" quantity to '
            f'{cart[product_id]}'
        )
    else:
        cart[product_id] = quantity
        messages.success(
            request,
            f'Added "{product.brand.friendly_name}: '
            f'{product.name}" to your cart'
        )

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, product_id):
    """
    A view to update the quantity of a specified product
    in the cart to a specified amount
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity'))
        print(quantity)
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[product_id] = quantity
            messages.success(
                request,
                f'Updated "{product.brand.friendly_name}: '
                f'{product.name}" quantity to '
                f'{cart[product_id]}'
            )
        else:
            cart.pop(product_id)
            messages.success(
                request,
                f'Removed "{product.brand.friendly_name}: '
                f'{product.name}" from your cart '
            )

        request.session['cart'] = cart
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error updating item: {e}')
        return HttpResponse(status=500)


def remove_from_cart(request, product_id):
    """
    A view to remove an item from the shopping cart
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        request.session['cart'] = cart
        messages.success(
                request,
                f'Removed "{product.brand.friendly_name}: '
                f'{product.name}" from your cart '
            )
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
