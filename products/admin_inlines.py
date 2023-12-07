from django.contrib import admin
from django.utils.html import format_html

from products.models import ProductMedia
from products.forms import ProductMediaForm


class ProductImageInline(admin.StackedInline):
    model = ProductMedia
    form = ProductMediaForm
    extra = 1
    fields = ['media', 'order']
