from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from checkout.models import Order
from shop.models import Product

from .models import UserProfile, UserWishlist
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    A view to display the current user's profile info.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'viewing_profile': True
    }

    return render(request, template, context)


@login_required
def orders(request):
    """
    A view to display the current user's order history.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all().order_by('-date')

    template = 'profiles/orders.html'
    context = {
        'orders': orders,
    }

    return render(request, template, context)


def previous_order(request, order_number):
    """
    A view to display a previous order of the current user.
    """
    order = get_object_or_404(Order, order_number=order_number)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def view_wishlist(request):
    """
    A view to display the current user's wishlist.
    """
    try:
        wishlist = UserWishlist.objects.get(user=request.user).product.all()
    except ObjectDoesNotExist:
        wishlist = None

    template = 'profiles/wishlist.html'
    context = {
        'wishlist': wishlist,
        'viewing_wishlist': True
    }

    return render(request, template, context)


@login_required
def update_wishlist(request, product_id):
    """
    A view to add/remove a chosen product to/from the current user's wishlist
    """
    product = get_object_or_404(Product, pk=product_id)
    request.session['updating_cart'] = False
    request.session['reviewing'] = False
    request.session['updating_product'] = False

    try:
        wishlist = UserWishlist.objects.get(user=request.user)
    except ObjectDoesNotExist:
        wishlist = UserWishlist.objects.create(user=request.user)

    try:
        if product in wishlist.product.all():
            wishlist.product.remove(product)
            messages.success(
                request,
                f'Removed "{product.brand.friendly_name}: '
                f'{product.name}" from your wishlist.'
            )
        else:
            wishlist.product.add(product)
            messages.success(
                request,
                f'Added "{product.brand.friendly_name}: '
                f'{product.name}" to your wishlist.'
            )

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error updating wishlist: {e}')
        return HttpResponse(status=500)
