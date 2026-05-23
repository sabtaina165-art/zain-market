from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def product_list(request):
    products   = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    query    = request.GET.get('q', '')
    cat_id   = request.GET.get('category', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if cat_id:
        products = products.filter(category_id=cat_id)

    return render(request, 'products/list.html', {
        'products':          products,
        'categories':        categories,
        'query':             query,
        'selected_category': cat_id,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'products/detail.html', {'product': product})


# ── Admin Product Management ─────────────────────────────────

def admin_required(view_func):
    """Decorator: only allow admin role users."""
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
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product add ho gaya!')
        return redirect('admin_products')
    return render(request, 'products/form.html', {'form': form, 'title': 'Product Add Karo'})


@login_required
@admin_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form    = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product update ho gaya!')
        return redirect('admin_products')
    return render(request, 'products/form.html', {'form': form, 'title': 'Product Edit Karo'})


@login_required
@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, 'Product remove ho gaya.')
        return redirect('admin_products')
    return render(request, 'products/confirm_delete.html', {'product': product})


@login_required
@admin_required
def admin_product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/admin_list.html', {'products': products})
