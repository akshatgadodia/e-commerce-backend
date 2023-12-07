from django.db import models

from common.models import BaseModel
from users.models import User
from products.models import Product


class Order(BaseModel):
    PROCESSING, SHIPPED, DELIVERED, RETURNED = 'PROCESSING', 'SHIPPED', 'DELIVERED', 'RETURNED'
    STATUS_CHOICES = (
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (RETURNED, 'Returned'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PROCESSING)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-date']

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['order', 'product']

    def __str__(self):
        return f"Item {self.id} - Order {self.order.id}, Product {self.product.name}"
