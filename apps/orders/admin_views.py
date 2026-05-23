from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from apps.products.models import Product
from apps.accounts.models import User
from .models import Order


def admin_required(view_func):
    from functools import wraps
    from django.http import HttpResponseForbidden
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user():
            return HttpResponseForbidden("Admin access only.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def dashboard(request):
    total_products  = Product.objects.filter(is_active=True).count()
    total_orders    = Order.objects.count()
    pending_orders  = Order.objects.filter(status='pending').count()
    total_revenue   = Order.objects.exclude(status='cancelled').aggregate(
                          total=Sum('total_amount'))['total'] or 0
    low_stock       = Product.objects.filter(stock__lte=5, is_active=True)
    recent_orders   = Order.objects.select_related('user').all()[:10]

    return render(request, 'dashboard/dashboard.html', {
        'total_products': total_products,
        'total_orders':   total_orders,
        'pending_orders': pending_orders,
        'total_revenue':  total_revenue,
        'low_stock':      low_stock,
        'recent_orders':  recent_orders,
    })


@login_required
@admin_required
def admin_order_list(request):
    query  = request.GET.get('q', '')
    orders = Order.objects.select_related('user').all()
    if query:
        orders = orders.filter(order_id__icontains=query)
    return render(request, 'dashboard/orders.html', {'orders': orders, 'query': query})


@login_required
@admin_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, 'Status update ho gaya!')
        return redirect('admin_order_detail', pk=pk)
    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })
