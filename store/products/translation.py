from modeltranslation.translator import register, TranslationOptions
from products.models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'brand', 'description', 'category')