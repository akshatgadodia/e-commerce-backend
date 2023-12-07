import requests
from decouple import config
from notifications.constants import CREATE_NOTIFICATION_URL
from common.logger import LogInfo
# from base.utils import generate_presigned_url


def create_notification(notification_content, subscriptions_ids, notification_title, campaign_name, notification_image):
    """
    Function to send or create notification by making use of one signal create_notification api
    """
    try:
        payload = {
            "include_subscription_ids": list(subscriptions_ids),
            "contents": {
                "en": notification_content,
            },
            "name": campaign_name,
            "app_id": config('ONE_SIGNAL_APP_ID'),
            "small_icon": "ic_stat_notifications_active",
        }
        if notification_title is not None:
            payload["headings"] = {
                "en": notification_title
            }
        if notification_image is not None:
            # image_url = generate_presigned_url(notification_image, expiration_time=604800)
            image_url = "hello"
            payload["big_picture"] = image_url
            payload["ios_attachments"] = image_url
        headers = {
            "accept": "application/json",
            "Authorization": f"Basic {config('ONE_SIGNAL_REST_API_KEY')}",
            "content-type": "application/json"
        }
        response = requests.post(CREATE_NOTIFICATION_URL, json=payload, headers=headers)
        response_data = response.json()
        if not response_data.get('id', None) or 'errors' in response_data:
            LogInfo.exception(response_data)
            return False
        response.raise_for_status()
        return True
    except Exception as exc:
        LogInfo.exception(exc)
        return False
