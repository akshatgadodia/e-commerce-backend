from django.urls import reverse

SENDING_NOTIFICATION = "Sending notification to {notification_for_id} - {subscription_id}"
SENDING_NOTIFICATION_SUCCESS = "Notification sent successfully!"
SENDING_NOTIFICATION_FAILED = "Cannot sent notification!"
TEMPLATE_NAME_NOT_UNIQUE = 'This template name is already taken! Please type another template name.'
NOTIFICATIONS_MARK_AS_READ = 'Notification are marked as read'
NOTIFICATIONS_INITIATED = 'Initiating the Sending of Broadcast Notifications'
SUBSCRIBER_ID_UPDATED = "Subscriber Id Updated Successfully"
SUBSCRIBER_ID_UPDATE_FAILED = "Failed To Update Subscriber Id"
NO_TEMPLATE_FOR_TRIGGER_POINT_TEMPLATE = (
    'No template for this trigger point is available. Please '
    '<a href="{}">click here</a> to create one.'
)


# Function to return the no template message formatted with url
def get_no_template_message():
    return NO_TEMPLATE_FOR_TRIGGER_POINT_TEMPLATE.format(reverse('admin:notifications_notificationtemplates_add'))

