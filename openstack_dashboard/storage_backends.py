from storages.backends.s3boto3 import S3Boto3Storage
import os
from datetime import datetime
import uuid

class MediaStorage(S3Boto3Storage):
    location = ''
    file_overwrite = False

def uploaded_filepath_custom(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join('ad74b43ed78b42d8b78c5c2c65881ab2:news','media', 'django-summernote', today, filename)