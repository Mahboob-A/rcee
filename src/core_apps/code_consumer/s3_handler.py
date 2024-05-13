# python
import logging

# django
from django.conf import settings

# other
import boto3
from botocore.exceptions import ClientError, UnknownEndpointError, UnknownKeyError


logger = logging.getLogger(__name__)


class S3DataHandler:
    """Handler class to interact with S3 Bucket to Download files"""

    def __get_client(self):
        return boto3.client("s3")

    def download_file_from_s3(self, bucket_name, object_key, file_name):
        # try:
        #     s3_client = self.__get_client()
        #     data = s3_client.download_file(bucket_name, object_key, file_name)
        #     print("\n[Download Success]: downloaded data: ", data)
        #     print("data type: ", type(data))
        # except Exception as e:
        #     print(
        #         "\n[Download Failed]: something gone wrong while downloading from s3: ",
        #         str(e),
        #     )

        try:
            s3 = boto3.client("s3")
            s3.head_object(Bucket=bucket_name, Key=object_key)
            data = s3.get_object(Bucket=bucket_name, Key=object_key)
            return data
        except ClientError as e:
            # if e.response['Error']['Code'] == '404' or e.response['Error']['Code'] == 'NoSuchKey':
            # missing file logic
            print(
                "\n[Download Failed]: something gone wrong while downloading from s3: ",
                str(e))
        else:
            raise e # or whatever you want


s3_data_handler = S3DataHandler()
