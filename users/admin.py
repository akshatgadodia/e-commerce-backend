from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from users.models import User, UserAddresses
from common.admin import BaseModelAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    ordering = ('name',)
    search_fields = ('name', 'email')
    empty_value_display = None
    show_full_result_count = False
    fieldsets = [
        (
            'Personal Info', {
                'fields': ('name', 'email', 'date_of_birth'),
            }
        ),
        (
            'Login Info', {
                'fields': ('password',),
                'classes': ('collapse',)
            }
        ),
        (
            'Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                'classes': ('collapse',)
            }
        ),
        (
            'Important Dates', {
                'fields': ('last_login', 'created_at', 'updated_at'),
                'classes': ('collapse',)
            }
        )
    ]


@admin.register(UserAddresses)
class UserAddressesAdmin(BaseModelAdmin):
    list_display = ('id', 'user_link', 'name', 'address', 'city_link', 'zip_code', 'mobile')
    ordering = ('name',)
    list_select_related = ('city', 'user')
    search_fields = ('user__name', 'city__city_name', 'zip_code')
    fieldsets = [
        (
            'Address', {
                'fields': ('user', 'name', 'address', 'city', 'zip_code', 'mobile'),
            }
        ),
    ]

    def user_link(self, obj):
        # This function returns a clickable link to the change form for the related user
        link = reverse('admin:users_user_change', args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', link, obj.user)
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__name'

    def city_link(self, obj):
        # This function returns a clickable link to the change form for the related city
        link = reverse('admin:locations_city_change', args=[obj.city_id])
        return format_html('<a href="{}">{}</a>', link, obj.city)
    city_link.short_description = 'City'
    city_link.admin_order_field = 'city__city_name'
