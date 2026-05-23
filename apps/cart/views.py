from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, pk):
    product  = get_object_or_404(Product, pk=pk, is_active=True)
    cart     = get_or_create_cart(request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f'Sirf {product.stock} items available hain.')
        return redirect('product_detail', pk=pk)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f'"{product.name}" cart mein add ho gaya!')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item     = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        item.delete()
        messages.info(request, 'Item cart se hata diya.')
    elif quantity > item.product.stock:
        messages.error(request, f'Sirf {item.product.stock} available hain.')
    else:
        item.quantity = quantity
        item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, 'Item hata diya.')
    return redirect('cart')


@login_required
def clear_cart(request):
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return redirect('cart')
