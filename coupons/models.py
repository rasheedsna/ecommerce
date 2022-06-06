import uuid
from django.db import models
from shop.models import Type


class Coupons(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    title = models.CharField(max_length=100)
    couponCode = models.CharField(max_length=10)
    endTime = models.DateTimeField()
    minimumAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    logo = models.ImageField(upload_to='coupon_banner')
    productType = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-updatedAt',)
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return '{}'.format(self.title)

