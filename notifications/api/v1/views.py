from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import serializers, status

from base.permissions import ApiPermission
from notifications.models import Notification
from notifications.messages import NOTIFICATIONS_MARK_AS_READ, SUBSCRIBER_ID_UPDATED, SUBSCRIBER_ID_UPDATE_FAILED
from notifications.api.v1.serializers import GetAllNotificationsSerializer
from base.generics import BaseListAPIView, BaseAPIView
from drf_yasg import openapi


class GetAllNotificationsView(BaseListAPIView):
    """
    View for listing all the notifications received by a user
    """
    queryset = Notification.objects.all()
    serializer_class = GetAllNotificationsSerializer
    ordering_fields = ('-created_at',)
    api_permissions = {'get': ["api_notification"]}
    permission_classes = [ApiPermission]

    def get_queryset(self):
        queryset = Notification.objects.get_all_notifications(self.request.user.tab_employee_id)
        return queryset


class MarkNotificationsAsReadView(BaseAPIView):
    serializer_class = serializers.Serializer
    api_permissions = {'patch': ["api_notification"]}
    permission_classes = [ApiPermission]

    @swagger_auto_schema(request_body=no_body)
    def patch(self, request):
        queryset = Notification.objects.get_all_notifications(request.user.tab_employee_id)
        queryset.update(is_read=True)
        return self.success_response(status_code=status.HTTP_200_OK, message=NOTIFICATIONS_MARK_AS_READ)


class SubscribeNotificationView(BaseAPIView):
    serializer_class = serializers.Serializer

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                    properties={
                                        "subscriber_id": openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                    )
    )
    def post(self, request):
        sub_id = request.data.get('subscriber_id', None)
        if sub_id:
            print(sub_id)
            request.user.subscriber_id = sub_id
            request.user.save()
            return self.success_response(message=SUBSCRIBER_ID_UPDATED, status_code=status.HTTP_200_OK)
        return self.failure_response(message=SUBSCRIBER_ID_UPDATE_FAILED, status_code=status.HTTP_400_BAD_REQUEST)
