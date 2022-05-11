from django.shortcuts import render


def index(request):
    """
    A view to return the index page
    """
    return render(
        request,
        'home/index.html',
        {'viewing_home': True}
    )


def handler404(request, exception):
    """
    404 error handler view
    """
    return render(request, 'home/404.html', status=404)


def handler500(request):
    """
    500 error handler view
    """
    return render(request, 'home/500.html', status=500)
