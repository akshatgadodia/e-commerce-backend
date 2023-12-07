from django.contrib import admin

from common.admin import BaseModelAdmin
from shipments.models import Shippers


@admin.register(Shippers)
class ShippersAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'contact', 'tracking_link')
    fieldsets = [
        ('Shipper', {
            'fields': ('name', 'contact', 'tracking_link'),
        }),
    ]

