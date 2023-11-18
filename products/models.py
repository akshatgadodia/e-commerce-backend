from django.db import models

from common.models import BaseModel
from products.managers import ProductDiscountManager, ProductManager


class ProductCategories(BaseModel):
    # Category name
    name = models.CharField(max_length=255)
    # Category description
    description = models.TextField()
    # Parent category (self-referential relationship for subcategories)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories',
                                        on_delete=models.CASCADE)

    def __str__(self):
        # String representation for ProductCategories
        return self.name

    class Meta:
        # Default ordering by name when querying the database
        ordering = ['name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'


class ProductInventory(BaseModel):
    # Current quantity of the product
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Minimum quantity threshold
    min_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Flag to determine if an alert should be sent when quantity is low
    send_alert = models.BooleanField(default=True)
    # Timestamp of the last alert sent
    last_alert_sent_on = models.DateTimeField(default=None, null=True, blank=True,
                                              help_text="Last time an alert was sent")

    def __str__(self):
        # String representation for ProductInventory
        return f"Inventory for {self.product.name}" if hasattr(self, 'product') else f"Inventory {self.id}"

    class Meta:
        # Default ordering by id when querying the database
        ordering = ['id']
        verbose_name = 'Product Inventory'
        verbose_name_plural = 'Product Inventories'


class ProductDiscount(BaseModel):
    # Discount name
    name = models.CharField(max_length=255)
    # Discount description
    description = models.TextField()
    # Percentage discount
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    # Unique discount code
    code = models.CharField(max_length=20, unique=True)
    # Expiry date of the discount
    expires_on = models.DateTimeField(default=None, null=True, blank=True, help_text="Expiry date of the discount")
    # Flag to determine if the discount is hidden
    hidden = models.BooleanField(default=True)
    # Discount is active or not
    active = models.BooleanField(default=True)

    # Overriding the default manager
    objects = ProductDiscountManager()

    def __str__(self):
        # String representation for ProductDiscount
        return f"{self.name} ({self.discount_percent}%)"

    class Meta:
        # Default ordering by name when querying the database
        ordering = ['name']
        verbose_name = 'Product Discount'
        verbose_name_plural = 'Product Discounts'


class Product(BaseModel):
    # Product name
    name = models.CharField(max_length=255)
    # Product description
    description = models.TextField()
    # Category to which the product belongs
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    # One-to-one relationship with product inventory
    inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE)
    # Discount applicable to the product
    discount = models.ManyToManyField(ProductDiscount, blank=True)
    # Product is active or not
    active = models.BooleanField(default=True)

    # Overriding the default manager
    objects = ProductManager()

    def __str__(self):
        # String representation for Product
        return f"{self.name} ({self.category.name})"

    class Meta:
        # Default ordering by name when querying the database
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
