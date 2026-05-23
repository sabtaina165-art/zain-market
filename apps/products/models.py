from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image_url   = models.URLField(blank=True)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    LOW_STOCK_THRESHOLD = 5

    @property
    def is_low_stock(self):
        return self.stock <= self.LOW_STOCK_THRESHOLD

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://placehold.co/400x300?text=No+Image'

    def __str__(self):
        return self.name
