from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from locations.models import Country, State, City
from common.admin import BaseModelAdmin


@admin.register(Country)
class CountryAdmin(BaseModelAdmin):
    list_display = ('country_name', 'currency', 'currency_name', 'phone_code')
    search_fields = ['country_name']


@admin.register(State)
class StateAdmin(BaseModelAdmin):
    list_display = ('state_name', 'country_link',)
    search_fields = ['state_name', 'country_name']
    list_filter = ('country_name',)
    list_display_links = ('state_name',)

    def country_link(self, obj):
        # This function returns a clickable link to the change form for the related country
        link = reverse('admin:locations_country_change', args=[obj.country_id])
        return format_html('<a href="{}">{}</a>', link, obj.country.country_name)
    country_link.short_description = 'Country'
    country_link.admin_order_field = 'country_name'


@admin.register(City)
class CityAdmin(BaseModelAdmin):
    list_display = ('city_name', 'state_link', 'country_link',)
    search_fields = ['city_name', 'state_name', 'country_name']
    list_filter = ('state_name', 'country_name')

    def state_link(self, obj):
        # This function returns a clickable link to the change form for the related state
        link = reverse('admin:locations_state_change', args=[obj.state_id])
        return format_html('<a href="{}">{}</a>', link, obj.state_name)
    state_link.short_description = 'State'
    state_link.admin_order_field = 'state_name'

    def country_link(self, obj):
        # This function returns a clickable link to the change form for the related country
        link = reverse('admin:locations_country_change', args=[obj.country_id])
        return format_html('<a href="{}">{}</a>', link, obj.country_name)
    country_link.short_description = 'Country'
    country_link.admin_order_field = 'country_name'
