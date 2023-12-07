from django.conf import settings
from botocore.config import Config
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE

    def __init__(self, **settings):
        super().__init__(**settings)
        self.config = Config(
                s3={'addressing_style': self.addressing_style, 'use_accelerate_endpoint': True},
                signature_version=self.signature_version,
                proxies=self.proxies,
                retries={'max_attempts': 5},
                connect_timeout=10,
                read_timeout=10,
                max_pool_connections=10,
        )