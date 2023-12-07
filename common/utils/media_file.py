import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage

from common.logger import LogInfo


def save_file(file, file_dir):
    """
    Save file to the default media folder
    args:
        file: file object to be saved
        file_dir: directory name to be stored in
    """
    try:
        filename = str(uuid.uuid4()) + "." + file.name.split('.')[-1]
        if settings.STORE_MEDIA_IN_S3:
            return default_storage.save(f"{file_dir}/{filename}", file)
        else:
            dir_path = os.path.join(settings.MEDIA_ROOT, file_dir)
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            return default_storage.save(os.path.join(file_dir, filename), file)
    except Exception as exc:
        LogInfo.exception(exc)
        return False


def delete_file(file_name):
    try:
        if settings.STORE_MEDIA_IN_S3:
            # s3_client = get_s3_client_object()
            # s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
            pass
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        LogInfo.exception(e)
        print(f"Error deleting file: {str(e)}")
