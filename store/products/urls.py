from django.urls import include, path

from products.views import *

app_name = 'products'


urlpatterns = [
    # Store main page
    path('', HomeView.as_view(), name='home'),
    # Products Page
    path('products/', ProductsListView.as_view(), name='product'),
    # Pagination
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    # Individual product
    path('product/<slug:product_slug>/', product_info, name='product-info'),
    # Individual category
    path('category/<slug:category_slug>/', ListCategoryView.as_view(), name='list-category'),

    path('add-review/<int:product_id>/', add_review, name='add_review'),
]



