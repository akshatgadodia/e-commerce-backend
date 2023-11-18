from django.db import models


class ProductDiscountManager(models.Manager):
    """
    Custom Manager for Product Discount Model
    """

    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def get_all_non_deleted_queryset(self):
        return super().get_queryset()


class ProductManager(models.Manager):
    """
    Custom Manager for Product Model
    """

    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def get_all_non_deleted_queryset(self):
        return super().get_queryset()