import uuid
from django.db import models
from shop.models import Product
from accounts.models import UserProfile


class Order(models.Model):
    STATUS_CHOICES = [
        ('Delivered', 'Delivered'),
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Cancel', 'Cancel')
    ]

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    contact = models.CharField(max_length=20)
    paymentMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    subTotal = models.DecimalField(max_digits=10, decimal_places=2)
    shippingCost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updatedAt',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return '{}'.format(self.name)


class Cart(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    itemTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-updatedAt',)
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return '{}'.format(self.product.title)
    