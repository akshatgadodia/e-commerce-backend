from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from notifications.models import Notification, NotificationTemplates, BroadcastNotification
from notifications.forms import NotificationTemplateForm
from notifications.constants import NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES
from notifications.actions import broadcast_notification
from common.admin import BaseModelAdmin


@admin.register(Notification)
class NotificationAdmin(BaseModelAdmin):
    list_display = ('id',  'campaign_name', 'notification_for_link', 'title', 'content', 'status',
                    'subscription_id', 'created_at',)
    list_select_related = ('notification_for',)
    search_fields = ('id', 'notification_for__employee_name', 'notification_for__name', 'title', 'content')
    list_filter = ('status', 'campaign_name')
    ordering = ('-created_at',)

    def notification_for_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.notification_for_id])
        return format_html(f'<a href="{url}">{obj.notification_for}</a>')
    notification_for_link.short_description = 'Notification For'
    notification_for_link.admin_order_field = 'notification_for__employee_name'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(NotificationTemplates)
class NotificationTemplateAdmin(BaseModelAdmin):
    form = NotificationTemplateForm
    change_form_template = 'notifications/notification_templates_change_form.html'
    add_form_template = 'notifications/notification_templates_change_form.html'
    list_display = ('id', 'module_name',  'trigger_point', 'template_name_link', 'is_active')
    fieldsets = (
        (
            None, {
                'fields': ('module_name', 'trigger_point', 'template_name', 'template_title', 'template_content',
                           'is_active',)
            }
        ),
    )

    class Media:
        js = ('notifications/js/custom_template_content_widget.js',)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['trigger_points'] = NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES
        return super(NotificationTemplateAdmin, self).add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['trigger_points'] = NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES
        return super(NotificationTemplateAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def template_name_link(self, obj):
        url = reverse('admin:notifications_notificationtemplates_change', args=[obj.id])
        return format_html(f'<a href="{url}">{obj.template_name}</a>')
    template_name_link.short_description = 'Template Title'
    template_name_link.admin_order_field = 'template_title'


@admin.register(BroadcastNotification)
class BroadcastNotificationAdmin(BaseModelAdmin):
    """
    Admin to Broadcast Notifications
    """
    list_display = ('id', 'name', 'email',)
    list_display_links = ('id',)
    search_fields = ('name',)
    ordering = ('name',)
    actions = (broadcast_notification,)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Select users to broadcast notification"
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        js = ('notifications/js/broadcast_notification.js',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return (queryset.prefetch_related('user_set').exclude(user__subscriber_id='')
    #             .filter(user__subscriber_id__isnull=False, user__is_active=True))
