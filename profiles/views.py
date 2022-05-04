from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from checkout.models import Order

from .models import UserProfile
from .forms import UserProfileForm


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


def orders(request):
    """
    A view to display the current user's order history.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

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
