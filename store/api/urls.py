from django.urls import include, path
from rest_framework import routers

from api.views import CategoryModelViewSet, ProductModelViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'categories', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]