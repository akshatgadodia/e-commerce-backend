from django.utils import timezone
from django.contrib.sessions.models import Session


def force_logout_user(user):
    # Deleting Sessions
    session_keys_to_delete = [
        session.session_key
        for session in Session.objects.all()
        if session.get_decoded().get('_auth_user_id') == user.id
    ]
    Session.objects.filter(session_key__in=session_keys_to_delete).delete()

    # Updating force logout for API's
    user.forced_logout_time = timezone.now()
    user.save()


