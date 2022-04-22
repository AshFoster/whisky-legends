from django.shortcuts import render, redirect, reverse


def view_cart(request):
    """ A view to return the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """
    A view to add a chosen quantity of a specified
    product to the cart
    """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, product_id):
    """
    A view to update the quantity of a specified product
    in the cart to a specified amount
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
