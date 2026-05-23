from django.urls import path
from . import views

urlpatterns = [
    path('',                       views.product_list,       name='product_list'),
    path('product/<int:pk>/',      views.product_detail,     name='product_detail'),
    path('manage/products/',       views.admin_product_list, name='admin_products'),
    path('manage/products/add/',   views.product_create,     name='product_create'),
    path('manage/products/<int:pk>/edit/',   views.product_edit,   name='product_edit'),
    path('manage/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
