import random
import string
from django.db import models
from django.conf import settings
from apps.products.models import Product


def generate_order_id():
    chars = string.ascii_uppercase + string.digits
    return 'ZM-' + ''.join(random.choices(chars, k=8))


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    order_id         = models.CharField(max_length=20, unique=True, default=generate_order_id)
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount     = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Delivery info
    delivery_name    = models.CharField(max_length=100)
    delivery_phone   = models.CharField(max_length=20)
    delivery_address = models.TextField()
    delivery_city    = models.CharField(max_length=100)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)   # snapshot
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
