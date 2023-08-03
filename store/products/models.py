from django.db.models import Avg
from django.utils import timezone
from django.db import models
from django.urls import reverse
from user_account.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:list-category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    brand = models.CharField(max_length=128, default='un-branded')
    description = models.TextField(max_length=256, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/',  null=True, blank=True, default='default_image.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', null=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product-info', args=[self.slug])


class Review(models.Model):
    STARS_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=STARS_CHOICES)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


