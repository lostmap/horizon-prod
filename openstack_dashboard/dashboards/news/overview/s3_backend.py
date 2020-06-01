import os
import boto3
from pathlib import Path
from botocore.client import Config
from django.conf import settings

#AWS_S3_REGION_NAME = 'RegionOne'
#AWS_S3_VERIFY = False
#AWS_S3_ENDPOINT_URL = 'https://localhost/'
#AWS_ACCESS_KEY_ID = '2dff69e63984445c819a1a3c3328bf8b'
#AWS_SECRET_ACCESS_KEY = '9bbe336440c94b079a19bb7b89aec749'

class S3Sync:
    """
    Class that holds the operations needed for synchronize local dirs to a given bucket.
    """

    def __init__(self):
        self._s3 = boto3.client('s3',
			config=Config(connect_timeout=5, retries={'max_attempts': 0}),
                        region_name=settings.AWS_S3_REGION_NAME,
                        verify=settings.AWS_S3_VERIFY,
                        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    def sync_to(self, source, dest):
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param source: Source folder.
        :param dest: Destination folder.

        :return: None
        """

        paths = self.list_source_objects(source_folder=source)
        
        objects = self.list_bucket_objects(dest)
        object_keys = [obj['Key'] for obj in objects]
        
        diff_keys = set(paths) - set(object_keys)
        
        for path in diff_keys:
            self._s3.upload_file(Filename=str(Path(source).joinpath(path)),  Bucket=dest, Key=path)

    def sync_from(self, source, dest):
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param source: Source folder.
        :param dest: Destination folder.

        :return: None
        """

        paths = self.list_source_objects(source_folder=dest)
        
        objects = self.list_bucket_objects(source)
        object_keys = [obj['Key'] for obj in objects]
        
        diff_keys = set(object_keys) - set(paths)

        for path in diff_keys:
            if not os.path.exists(os.path.dirname(str(Path(dest).joinpath(path)))):
                os.makedirs(os.path.dirname(str(Path(dest).joinpath(path))))
            self._s3.download_file(Bucket=source, Key=path, Filename=str(Path(dest).joinpath(path)))

    def list_bucket_objects(self, bucket):
        """
        List all objects for the given bucket.

        :param bucket: Bucket name.
        :return: A [dict] containing the elements in the bucket.

        Example of a single object.

        {
            'Key': 'example/example.txt',
            'LastModified': datetime.datetime(2019, 7, 4, 13, 50, 34, 893000, tzinfo=tzutc()),
            'ETag': '"b11564415be7f58435013b414a59ae5c"',
            'Size': 115280,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'webfile',
                'ID': '75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
            }
        }

        """
        try:
            contents = self._s3.list_objects(Bucket=bucket)['Contents']
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return contents

    @staticmethod
    def list_source_objects(source_folder):
        """
        :param source_folder:  Root folder for resources you want to list.
        :return: A [str] containing relative names of the files.

        Example:

            /tmp
                - example
                    - file_1.txt
                    - some_folder
                        - file_2.txt

            >>> sync.list_source_objects("/tmp/example")
            ['file_1.txt', 'some_folder/file_2.txt']

        """

        path = Path(source_folder)

        paths = []

        for file_path in path.rglob("*"):
            if file_path.is_dir():
                continue
            str_file_path = str(file_path)
            str_file_path = str_file_path.replace("{to}/".format(to=str(path)), "")
            paths.append(str_file_path)

        return paths
