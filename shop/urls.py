from django.urls import path
from . import views

urlpatterns = [
    path('', views.Shop.as_view(), name='shop'),
    path('<product_id>', views.product_detail, name='product_detail'),
    path('delete_review/<review_id>', views.delete_review,
         name='delete_review'),
]
