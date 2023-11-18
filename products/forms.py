from django import forms
from django.shortcuts import get_object_or_404

from products.models import Product, ProductInventory
from products.messages import QUANTITY_AND_MIN_QUANTITY_REQUIRED


class ProductForm(forms.ModelForm):
    # Current quantity of the product
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    # Minimum quantity threshold
    min_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    # Flag to determine if an alert should be sent when quantity is low
    send_low_inventory_alert = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            product = get_object_or_404(Product, id=self.instance.pk)
            product_inventory_data = ProductInventory.objects.get(product=product)
            self.initial['quantity'] = product_inventory_data.quantity
            self.initial['min_quantity'] = product_inventory_data.min_quantity
            self.initial['send_low_inventory_alert'] = product_inventory_data.send_alert

    def clean(self):
        cleaned_data = super().clean()
        send_alert = cleaned_data.get('send_low_inventory_alert')
        quantity = cleaned_data.get('quantity')
        min_quantity = cleaned_data.get('min_quantity')

        if send_alert and not (quantity and min_quantity):
            self.add_error('send_low_inventory_alert', QUANTITY_AND_MIN_QUANTITY_REQUIRED)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'quantity', 'min_quantity', 'send_low_inventory_alert', 'discount']
