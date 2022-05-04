from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('orders/<order_number>', views.previous_order, name='previous_order'),
]
