from django.contrib import admin
from django.utils import timezone
from django.contrib.sessions.models import Session

from common.logger import LogInfo


@admin.action(description="Force Logout Users")
def force_logout_users(modeladmin, request, queryset):
    try:
        # Update forced_logout_time to now for selected users
        queryset.update(forced_logout_time=timezone.now())

        # Collect session keys for selected users
        user_ids = queryset.values_list('id', flat=True)
        session_keys_to_delete = [
            session.session_key
            for session in Session.objects.all()
            if int(session.get_decoded().get('_auth_user_id')) in user_ids
        ]
        # Bulk delete sessions
        Session.objects.filter(session_key__in=session_keys_to_delete).delete()
    except Exception as e:
        LogInfo.exception(e)
        print(e)

