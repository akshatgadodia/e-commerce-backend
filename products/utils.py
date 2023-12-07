import os
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class UniqueFilename(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{instance.product.id}-{uuid.uuid4()}.{ext}"
        return os.path.join('uploads', 'products_media', filename)
