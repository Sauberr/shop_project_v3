from http import HTTPStatus
from products.models import Product, Category

from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):

    def test_view(self):
        path = reverse('products:home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'IGUS Online Sports Store')
        self.assertTemplateUsed(response, 'products/home.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:product')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:6]))

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Clothes')
        self.assertTemplateUsed(response, 'products/product.html')


class ListCategoryViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.category = Category.objects.get(slug='t-shirt')
        self.products = Product.objects.filter(category=self.category)

    def test_list_category_view(self):
        path = reverse('products:list-category', args=[self.category.slug])
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context['object_list']), list(self.products))

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Category page')
        self.assertTemplateUsed(response, 'products/list_category.html')


