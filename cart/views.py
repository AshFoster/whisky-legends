from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Product
from profiles.models import UserWishlist


def view_cart(request):
    """
    A view to return the shopping cart page
    """
    if request.user.is_anonymous:
        wishlist = None
    else:
        try:
            wishlist = UserWishlist.objects.get(
                user=request.user).product.all()
        except ObjectDoesNotExist:
            wishlist = None

    template = 'cart/cart.html'
    context = {
        'wishlist': wishlist,
        'viewing_cart': True,
    }

    return render(request, template, context)


def add_to_cart(request, product_id):
    """
    A view to add a chosen quantity of a specified
    product to the cart
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        request.session.get('updating_cart', True)
        request.session['updating_cart'] = True

        if product_id in list(cart.keys()):
            if cart[product_id] >= 99 and quantity == 1:
                messages.error(
                    request,
                    f'There are already {cart[product_id]} '
                    f'"{product.brand.friendly_name}: {product.name}" '
                    f'in your cart! You cannot add any more.'
                )
            else:
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
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error adding to cart: {e}')
        return HttpResponse(status=500)


def update_cart(request, product_id):
    """
    A view to update the quantity of a specified product
    in the cart to a specified amount
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        request.session.get('updating_cart', True)
        request.session['updating_cart'] = True

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
        request.session.get('updating_cart', True)
        request.session['updating_cart'] = True
        messages.success(
                request,
                f'Removed "{product.brand.friendly_name}: '
                f'{product.name}" from your cart '
            )
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
