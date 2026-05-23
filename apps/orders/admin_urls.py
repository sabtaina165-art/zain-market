from django.urls import path
from .admin_views import dashboard, admin_order_list, admin_order_detail

urlpatterns = [
    path('',                      dashboard,           name='admin_dashboard'),
    path('orders/',               admin_order_list,    name='admin_order_list'),
    path('orders/<int:pk>/',      admin_order_detail,  name='admin_order_detail'),
]
