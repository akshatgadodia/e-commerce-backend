from django.db import models
from notifications.tasks import send_notifications


class NotificationLogsManager(models.Manager):
    def notify_bulk_create(self, objs, **kwargs):
        """
        Custom bulk create function which saves the notifications in bulk along with calling method to send those
        notification in background using celery
        """
        data = self.bulk_create(objs, **kwargs)
        notifications = [notification.id for notification in data]
        send_notifications.delay(notifications)
        return data

    def get_all_notifications(self, tab_employee_id):
        return self.get_queryset().filter(notification_for_id=tab_employee_id, status=self.model.SUCCESS)


class NotificationTemplatesManager(models.Manager):

    def get_queryset(self):
        """
        Override the default queryset to only return non-deleted notification templates
        """
        return super().get_queryset().filter(is_deleted=False)

    def get_active_template_for_trigger_point(self, trigger_point):
        """
        Queryset to retrieve active templates for a trigger point
        """
        return self.get_queryset().filter(is_active=True, trigger_point=trigger_point)
