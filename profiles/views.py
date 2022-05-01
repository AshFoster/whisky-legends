from django.shortcuts import render


def profile(request):
    """
    A view to display the current user's profile.
    """

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
