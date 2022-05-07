from django.urls import path
from . import views

urlpatterns = [
    path('', views.Shop.as_view(), name='shop'),
    path('<product_id>', views.product_detail, name='product_detail')
]
