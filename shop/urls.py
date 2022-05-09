from django.urls import path
from . import views

urlpatterns = [
    path('', views.Shop.as_view(), name='shop'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete_review/<review_id>/', views.delete_review,
         name='delete_review'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product,
         name='edit_product'),
]
