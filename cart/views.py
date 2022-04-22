from django.shortcuts import render, redirect, reverse, HttpResponse


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
    try:
        quantity = int(request.POST.get('quantity'))
        print(quantity)
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id)

        request.session['cart'] = cart
        # return redirect(reverse('view_cart'))
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)


def remove_from_cart(request, product_id):
    """
    A view to remove an item from the shopping cart
    """
    try:
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
