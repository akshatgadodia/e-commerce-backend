from django.urls import path
from notifications.api.v1 import views

urlpatterns = [
    path("", views.GetAllNotificationsView.as_view()),
    path("read/", views.MarkNotificationsAsReadView.as_view()),
    path("subscribe/", views.SubscribeNotificationView.as_view()),
]
