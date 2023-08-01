from django.db import models
from django.db.models import Avg
from django.urls import reverse


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

    def average_rating(self):
        return self.ratings.aggregate(Avg('value'))['value__avg'] or 0

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product-info', args=[self.slug])


class RatingStar(models.Model):
    value = models.SmallIntegerField('Value', default=0)
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name_plural = 'rating stars'
        verbose_name = 'rating stars'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('IP address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')

    def __str__(self):
        return f'{self.star} - {self.product}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Rating'


