import logging
import traceback
from django.conf import settings


DEBUG = settings.DEBUG


class LogInfo(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def configure_logger(logger_name):
        return logging.getLogger(logger_name)

    @staticmethod
    def print_to_console(msg):
        if DEBUG:
            print(msg)

    @staticmethod
    def debug(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('debug_logger')
        # LogInfo.print_to_console(msg)
        logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('info_logger')
        # LogInfo.print_to_console(msg)
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('error_logger')
        LogInfo.print_to_console(msg)
        logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('error_logger')
        stack_trace = traceback.format_exc()
        LogInfo.print_to_console(f"{msg}\n{stack_trace}")
        logger.exception(msg, *args, **kwargs)

    @staticmethod
    def celery_log_info(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('celery')
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def email_log_info(msg, *args, **kwargs):
        logger = LogInfo.configure_logger('email')
        logger.info(msg, *args, **kwargs)
