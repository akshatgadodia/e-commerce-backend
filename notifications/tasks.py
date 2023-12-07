from celery import shared_task
from django.apps import apps
from notifications.one_signal import create_notification
from common.logger import LogInfo
from notifications.messages import SENDING_NOTIFICATION
import concurrent.futures


@shared_task()
def send_notifications(notifications):
    notification_model = apps.get_model('notifications.Notification')
    try:
        queryset = notification_model.objects.filter(id__in=notifications)
        updated_notification_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}

            for notification in queryset:
                LogInfo.celery_log_info(
                    SENDING_NOTIFICATION.format(notification_for_id=notification.notification_for_id,
                                                subscription_id=notification.subscription_id))
                fs = executor.submit(create_notification, notification.content, [notification.subscription_id],
                                     notification.title, notification.campaign_name, notification.image)
                futures[fs] = notification

            for future in concurrent.futures.as_completed(futures):
                notification = futures[future]
                notification.status = notification_model.SUCCESS if future.result() else notification_model.FAILED
                updated_notification_list.append(notification)
            queryset.bulk_update(updated_notification_list, ['status'])
    except Exception as e:
        LogInfo.exception(e)
