from django.db import models

from products.models import Product
from user_account.models import User


class ShippingAddress(models.Model):

    DoesNotExist = None
    full_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'
        verbose_name = 'Shipping Address'

    def __str__(self):
        return 'Shipping Address - ' + str(self.id)


class Order(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Order'
        verbose_name = 'Order'

    def __str__(self):
        return 'Order - #' + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'OrderItem'
        verbose_name = 'OrderItem'

    def __str__(self):
        return 'Order Item - #' + str(self.id)