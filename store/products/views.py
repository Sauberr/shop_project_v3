from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView, ListView

from common.views import TitleMixin
from products.models import Category, Product


class HomeView(TitleMixin, TemplateView):
    template_name = 'products/home.html'
    title = 'IGUS Online Sports Store'

# def home(request):
#     context = {
#         'title': 'IGUS Online Sports Store'
#     }
#     return render(request, 'products/home.html', context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'products'
    paginate_by = 6
    title = 'Clothes'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(Q(name__icontains=search))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        paginator = context['paginator']
        page_number = self.request.GET.get('page')
        try:
            products_paginator = paginator.get_page(page_number)
        except EmptyPage:
            products_paginator = paginator.get_page(1)
            message = "This page does not contain any results."
        else:
            message = ""

        context['search'] = search
        context['message'] = message
        context['products'] = products_paginator
        return context


#
# def products(request, page_number=1):
#     # Search
#     search = request.GET.get('search')
#     product = Product.objects.all()
#
#     products = product.filter(name__icontains=search) if search else Product.objects.all()
#
#     # Pagination
#     per_page = 6
#     paginator = Paginator(products, per_page)
#
#     message = ""
#
#     try:
#         products_paginator = paginator.page(page_number)
#     except EmptyPage:
#         products_paginator = paginator.page(1)
#         message = "This page does not contain any results."
#
#     context = {
#         'title': 'Clothes',
#         'products': products_paginator,
#         'search': search,
#         'message': message,
#     }
#     return render(request, 'products/product.html', context)


class ProductDetailView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_info.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    title = 'Product detail page'


# def product_info(request, product_slug):
#     context = {'product': get_object_or_404(Product, slug=product_slug), 'title': 'Product detail page'}
#     return render(request, 'products/product_info.html', context)


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


class ListCategoryView(TitleMixin, ListView):
    model = Product
    template_name = 'products/list_category.html'
    context_object_name = 'products'
    title = 'Category page'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)

        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(ListCategoryView, self).get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        context['category'] = category
        return context


# def list_category(request, category_slug=None):
#     category = get_object_or_404(Category, slug=category_slug)
#     products = Product.objects.filter(category=category)
#     context = {'category': category, 'products': products, 'title': 'Category page'}
#     return render(request, 'products/list_category.html', context)
