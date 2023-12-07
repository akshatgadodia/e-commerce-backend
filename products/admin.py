from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.functional import SimpleLazyObject

from common.admin import BaseModelAdmin
from products.admin_inlines import ProductImageInline
from products.models import ProductCategories, ProductInventory, ProductDiscount, Product
from products.forms import ProductForm, ProductCategoriesForm


@admin.register(ProductCategories)
class ProductCategoriesAdmin(BaseModelAdmin):
    form = ProductCategoriesForm
    list_display = ('name', 'description', 'parent_category_link')
    search_fields = ('name',)
    list_select_related = ('parent_category',)
    fieldsets = [
        (
            'Product Category', {
                'fields': ('name', 'parent_category', 'description',),
            }
        ),
    ]

    def parent_category_link(self, obj):
        if obj.parent_category_id:
            link = reverse('admin:products_productcategories_change', args=[obj.parent_category_id])
            return format_html('<a href="{}">{}</a>', link, obj.parent_category)
        return None
    parent_category_link.short_description = 'Parent Category'


@admin.register(ProductDiscount)
class ProductDiscountAdmin(BaseModelAdmin):
    list_display = ['name', 'description', 'discount_percent', 'code', 'expires_on', 'hidden', 'active']
    list_filter = ('hidden', 'active')
    search_fields = ['name', 'code']
    fieldsets = [
        (
            'Product Discount', {
                'fields': ('name', 'description', 'discount_percent', 'code', 'expires_on', 'hidden', 'active'),
            }
        ),
    ]

    def get_queryset(self, request):
        return ProductDiscount.objects.get_all_non_deleted_queryset()


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    form = ProductForm
    list_display = ['name', 'category_link', 'quantity_available', 'minimum_quantity',
                    'send_low_inventory_alert', 'active']
    list_filter = ('category', 'active', 'inventory__send_alert')
    search_fields = ['name', 'category__name']
    list_select_related = ('category', 'inventory')
    filter_horizontal = ('discount',)
    inlines = (ProductImageInline,)
    fieldsets = [
        ('Product Info', {
            'fields': ('name', 'category', 'description', 'active')
        }),
        ('Inventory Info', {
            'fields': ('quantity', 'min_quantity', 'send_low_inventory_alert')
        }),
        ('Discounts', {
            'fields': ('discount',)
        }),
    ]

    def get_queryset(self, request):
        return Product.objects.get_all_non_deleted_queryset()

    def category_link(self, obj):
        link = reverse('admin:products_productcategories_change', args=[obj.category_id])
        return format_html('<a href="{}">{}</a>', link, obj.category)
    category_link.short_description = 'Category'
    category_link.admin_order_field = 'category__name'

    def quantity_available(self, obj):
        return obj.inventory.quantity
    quantity_available.short_description = 'Quantity Available'
    quantity_available.admin_order_field = 'inventory__quantity'

    def minimum_quantity(self, obj):
        return obj.inventory.min_quantity
    minimum_quantity.short_description = 'Minimum Quantity'
    minimum_quantity.admin_order_field = 'inventory__min_quantity'

    def send_low_inventory_alert(self, obj):
        return obj.inventory.send_alert
    send_low_inventory_alert.boolean = True
    send_low_inventory_alert.short_description = 'Send Low Inventory Alert'
    send_low_inventory_alert.admin_order_field = 'inventory__send_alert'

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to handle saving both Product and ProductInventory instances.
        """
        # Get or create ProductInventory instance
        product_inventory, created = ProductInventory.objects.get_or_create(product=obj)
        # Update ProductInventory fields
        product_inventory.quantity = form.cleaned_data['quantity']
        product_inventory.min_quantity = form.cleaned_data['min_quantity']
        product_inventory.send_alert = form.cleaned_data['send_low_inventory_alert']
        # Getting User
        user = request.user if not isinstance(request.user, SimpleLazyObject) else None
        if change:
            product_inventory.updated_by = user
        else:
            product_inventory.created_by = user
        product_inventory.save()  # Saving Product Inventory
        obj.inventory = product_inventory
        super(ProductAdmin, self).save_model(request, obj, form, change)
