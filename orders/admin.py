from django.contrib import admin

from orders.models import Order, OrderItems
from common.admin import BaseModelAdmin
from shipments.models import Shipment


class ShipmentInline(admin.StackedInline):
    model = Shipment
    max_num = 1
    can_delete = False
    fields = ('shipper', 'tracking_number', 'shipment_date', 'shipment_received_date')


class OrderItemInline(admin.TabularInline):
    model = OrderItems
    fields = ('product', 'quantity', 'sub_total')
    readonly_fields = ('product', 'quantity', 'sub_total')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    inlines = [OrderItemInline, ShipmentInline]
    list_display = ('user', 'date', 'total_amount', 'status',)
    list_select_related = ('user',)
    readonly_fields = ('user', 'date', 'total_amount')
    fieldsets = [
        ('Order Information', {
            'fields': ('user', 'date', 'total_amount', 'status'),
        }),
    ]
