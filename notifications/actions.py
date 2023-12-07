from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from common.utils import save_file
from notifications.models import Notification
from notifications.forms import NotificationForm
from notifications.messages import NOTIFICATIONS_INITIATED
from notifications.constants import (NOTIFICATION_CAMPAIGN_NAME, CUSTOM_NOTIFICATION,
                                     NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES)
import json


@admin.action(description="Broadcast Notification")
def broadcast_notification(modeladmin, request, queryset):
    """
    Custom Admin Action to send notification to all the selected employees
    """
    if 'apply' in request.POST:
        form = NotificationForm(request.POST, request.FILES)  # Include request.FILES for file upload
        if form.is_valid():
            notification_title = form.cleaned_data["notification_title"]
            notification_content = form.cleaned_data["notification_content"]
            notification_image = form.cleaned_data["notification_image"]
            filename = None
            if notification_image:
                saved_file = save_file(notification_image, 'temp/notifications')
                if saved_file:
                    filename = saved_file

            notifications = []
            for query in queryset:
                user_set = query.user_set.filter(is_active=True).first()
                if user_set.subscriber_id:
                    notifications.append(
                        Notification(
                            created_by_id=request.user.tab_employee_id,
                            notification_for=query,
                            title=notification_title.format(employee_name=query.employee_name),
                            content=notification_content.format(employee_name=query.employee_name),
                            subscription_id=user_set.subscriber_id,
                            campaign_name=NOTIFICATION_CAMPAIGN_NAME,
                            image=filename
                        )
                    )

            Notification.objects.notify_bulk_create(notifications)
            messages.add_message(request, messages.INFO, NOTIFICATIONS_INITIATED)
            return HttpResponseRedirect(request.get_full_path())

    opts = modeladmin.model._meta
    form = NotificationForm(initial={'_selected_action': queryset.values_list('name', flat=True)})
    context = admin.site.each_context(request)

    extra_context = {
        'title': 'Broadcast a Notification',
        'opts': opts,
        'items': queryset.values_list('employee_name', flat=True).order_by('employee_name').distinct(),
        'form': form,
        'breadcrumb_title': 'Broadcast Notifications',
        'action_name': 'broadcast_notification',
        'dynamic_variables': json.dumps(NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES[CUSTOM_NOTIFICATION])
    }
    context.update(extra_context)
    return render(request, "notifications/action_broadcast_notification_templates.html", context)
