from rest_framework import serializers
from notifications.models import Notification


class GetAllNotificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for get all user notifications
    """

    class Meta:
        model = Notification
        fields = ('id', 'campaign_name', 'title', 'content', 'created_at', 'is_read')
