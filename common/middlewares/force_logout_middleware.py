from django.http import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework_simplejwt.tokens import UntypedToken

from common.logger import LogInfo
from common.messages import FORCE_LOGOUT_MESSAGE


class ForceLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Access the Authorization header from the request
        authorization_header = request.headers.get('Authorization', '')

        # Check if the header includes a JWT token
        if authorization_header.startswith('Bearer '):
            # Extract the token part after 'Bearer '
            token = authorization_header.split(' ')[1]
            # Decode the token to get its content
            try:
                decoded_token = UntypedToken(token)

                user = request.user
                forced_logout_time = user.forced_logout_time

                if forced_logout_time and decoded_token['iat'] < forced_logout_time.timestamp():
                    # Send a JSON response with 403 status
                    return JsonResponse({'status_code': HTTP_403_FORBIDDEN, 'message': FORCE_LOGOUT_MESSAGE,
                                         'data': {'force_logout': True}},
                                        status=403)
            except Exception as e:
                # Handle any exceptions that may occur during decoding
                LogInfo.exception(e)

        response = self.get_response(request)
        return response
