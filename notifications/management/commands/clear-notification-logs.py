from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from common.logger import LogInfo
from notifications.models import Notification
from notifications.management.commands._messages import NOTIFICATION_LOG_CLEAR_HELP, \
    NOTIFICATION_LOG_CLEAR_COMMAND_FAILURE_RESPONSE, NOTIFICATION_LOG_CLEAR_COMMAND_SUCCESS_RESPONSE, \
    NOTIFICATION_LOG_CLEAR_COMMAND_STARTED


class Command(BaseCommand):
    help = NOTIFICATION_LOG_CLEAR_HELP

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='Number of days past to clear notifications')

    def handle(self, *args, **kwargs):
        try:
            days = kwargs['days']
            self.stdout.write(NOTIFICATION_LOG_CLEAR_COMMAND_STARTED.format(days=days))
            past_date = timezone.now() - timedelta(days=days)
            logs_to_be_deleted = Notification.objects.filter(created_at__lt=past_date)
            count = logs_to_be_deleted._raw_delete(logs_to_be_deleted.db)
            self.stdout.write(NOTIFICATION_LOG_CLEAR_COMMAND_SUCCESS_RESPONSE.format(count=count))
        except Exception as e:
            LogInfo.exception(e)
            self.stdout.write(NOTIFICATION_LOG_CLEAR_COMMAND_FAILURE_RESPONSE)
