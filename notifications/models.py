from django.db import models

from common.models import BaseModel
from users.models import User
from notifications.managers import NotificationLogsManager, NotificationTemplatesManager
from notifications.constants import NOTIFICATION_CAMPAIGN_NAME, NOTIFICATION_TRIGGER_POINTS


# Create your models here.
class Notification(models.Model):
    SUCCESS, FAILED = "SUCCESS", "FAILED"
    STATUS_CHOICES = (
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when an object is created
    notification_for = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='notification_for',
                                         null=True)
    title = models.CharField(max_length=255, null=True)
    campaign_name = models.CharField(max_length=255, null=True, default=NOTIFICATION_CAMPAIGN_NAME)
    content = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=FAILED)
    subscription_id = models.CharField(max_length=40)
    image = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    # Override the default manager
    objects = NotificationLogsManager()

    class Meta:
        db_table = 'notification_logs'
        ordering = ('-created_at',)
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'

    def __str__(self):
        return f"{self.id}"


class NotificationTemplates(BaseModel):
    module_name = models.CharField(max_length=10, choices=list())
    trigger_point = models.CharField(max_length=50, choices=NOTIFICATION_TRIGGER_POINTS, db_index=True)
    template_name = models.CharField(max_length=50)
    template_content = models.CharField(max_length=255)
    template_title = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Override the default manager
    objects = NotificationTemplatesManager()

    class Meta:
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
        ordering = ('module_name', 'trigger_point',)

    def __str__(self):
        return self.template_name


class BroadcastNotification(User):
    """
    Proxy model of tabEmployee for the broadcast notifications admin
    """
    class Meta:
        managed = False
        proxy = True
        verbose_name = 'Broadcast Notification'
        verbose_name_plural = 'Broadcast Notifications'


class ApiPermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("api_notification", "Notification Get, Read"),
        )
