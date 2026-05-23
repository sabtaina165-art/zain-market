from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    try:
        cart = request.user.cart
    except Exception:
        return redirect('cart')

    if not cart.items.exists():
        messages.warning(request, 'Cart khaali hai.')
        return redirect('cart')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = Order.objects.create(
                user             = request.user,
                delivery_name    = form.cleaned_data['delivery_name'],
                delivery_phone   = form.cleaned_data['delivery_phone'],
                delivery_address = form.cleaned_data['delivery_address'],
                delivery_city    = form.cleaned_data['delivery_city'],
                total_amount     = cart.total,
            )
            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order        = order,
                    product      = item.product,
                    product_name = item.product.name,
                    quantity     = item.quantity,
                    unit_price   = item.product.price,
                )
                # Deduct stock
                item.product.stock -= item.quantity
                item.product.save()

            cart.items.all().delete()

        messages.success(request, f'Order place ho gaya! ID: {order.order_id}')
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
