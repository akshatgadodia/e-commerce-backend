from django.contrib import admin
from django.db import models
from django.urls import re_path
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.utils.functional import SimpleLazyObject

from common.models import SiteConfiguration
from common.constants import DEFAULT_SINGLETON_INSTANCE_ID


class BaseModelAdmin(admin.ModelAdmin):
    # Default options for all model admins
    empty_value_display = ''
    show_full_result_count = False

    def save_model(self, request, obj, form, change):
        user = request.user if not isinstance(request.user, SimpleLazyObject) else None
        if change:
            obj.updated_by_id = user
        else:
            obj.created_by_id = user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete(user=request.user)

    def delete_queryset(self, request, queryset):
        queryset.delete(user=request.user)


class SingletonModelAdmin(BaseModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        """
        Overridden default get_urls to display change form instead of List Display
        """
        urls = super(SingletonModelAdmin, self).get_urls()
        model_name = self.model._meta.model_name

        url_name_prefix = '%(app_name)s_%(model_name)s' % {
            'app_name': self.model._meta.app_label,
            'model_name': model_name,
        }
        custom_urls = [
            # Custom URLs for history and change views
            re_path(r'^history/$',
                    self.admin_site.admin_view(self.history_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_history' % url_name_prefix),
            re_path(r'^$',
                    self.admin_site.admin_view(self.change_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_change' % url_name_prefix),
        ]

        return custom_urls + urls

    def response_change(self, request, obj):
        """
        Overridden default response_change to redirect to home page instead of list display page
        """
        msg = _('%(obj)s was changed successfully.') % {'obj': force_str(obj)}
        if '_continue' in request.POST:
            # Continue editing the object
            self.message_user(request, msg + ' ' + _('You may edit it again below.'))
            return HttpResponseRedirect(request.path)
        else:
            # Redirect to home page after successful change
            self.message_user(request, msg)
            return HttpResponseRedirect("../../")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
         Overridden default change_view to display change form for the default singleton instance id
        """
        if object_id == str(self.singleton_instance_id):
            # Create the singleton instance if it doesn't exist
            self.model.objects.get_or_create(pk=self.singleton_instance_id)

        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def history_view(self, request, object_id, extra_context=None):
        """
        Overridden default change_view to display history of the default singleton instance id
        """
        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).history_view(
            request,
            object_id,
            extra_context=extra_context,
        )

    @property
    def singleton_instance_id(self):
        # Get the singleton instance id from the model, defaulting to DEFAULT_SINGLETON_INSTANCE_ID
        return getattr(self.model, 'singleton_instance_id', DEFAULT_SINGLETON_INSTANCE_ID)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    fieldsets = [
        (
            'Site Configurations', {
                'fields': ('bypass_api_permissions',)
            },
        ),
        (
            'APP Configurations', {
                'fields': ('min_android_version', 'min_ios_version', 'latest_android_version',
                           'latest_ios_version')
            },
        ),
    ]
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 5})},
    }

    def save_model(self, request, obj, form, change):
        # Set created_by and updated_by fields when saving the model
        obj.created_by_id = request.user
        if change:
            obj.updated_by_id = request.user
        super().save_model(request, obj, form, change)
