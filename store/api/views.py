from rest_framework.viewsets import ModelViewSet

from products.models import Category, Product
from products.permissions import IsAdminOrReadOnly
from products.serializers import CategorySerializer, ProductSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

