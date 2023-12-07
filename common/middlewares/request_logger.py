import time
from base.custom_logger import LogInfo


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        execution_time = time.time() - start_time
        # Log request details
        LogInfo.info(
            f"Method: {request.method}, "
            f"Path: {request.path}, "
            f"Headers: {request.headers}, "
            f"Device IP: {self.get_client_ip(request)}, "
            f"Response Status: {response.status_code}, "
            f"Execution Time: {execution_time:.6f} seconds"
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
