from django.contrib import admin

from products.models import Category, Product, Review
from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    fields = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name',)
    fields = (('name', 'slug'), 'brand', 'description', 'price', 'image', 'quantity', 'category')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fields = ('user', 'product', 'stars', 'text', 'created_at')



