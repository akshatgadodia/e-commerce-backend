from django.db import models

from common.models import BaseModel
from orders.models import Order


class Shippers(BaseModel):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    tracking_link = models.URLField()

    class Meta:
        verbose_name = 'Shipper'
        verbose_name_plural = 'Shippers'
        ordering = ['name']    # shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Shipment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    shipper = models.ForeignKey(Shippers, on_delete=models.DO_NOTHING)
    tracking_number = models.CharField(max_length=255)
    shipment_date = models.DateTimeField()
    shipment_received_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'
        ordering = ['-shipment_date']

    def __str__(self):
        return f"Shipment {self.id} - Tracking: {self.tracking_number}, Shipper: {self.shipper.name}"
