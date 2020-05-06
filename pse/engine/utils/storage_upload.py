from botocore.client import Config
from botocore.exceptions import ClientError
import boto3

ENDPOINT = "https://storage.yandexcloud.net"
ACCESS_KEY = "Kh_5cDVkTRoSHivFUvUA"
SECRET_KEY = "1VFz0tGxlDbEUxF4CtL29LE-JSuN5eyFfIfEWMM8"
STORAGE_NAME = "pdf-storage"

def init_client():
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="ru-central1",
    ) 
    s3 = session.client(
        service_name='s3',
        endpoint_url=ENDPOINT,
        config=Config(signature_version="s3v4")
    )

    return s3


def file2url(filename, filekey):
    s3_client = init_client()
    try: 
        s3_client.upload_file(filename, STORAGE_NAME, filekey)

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": STORAGE_NAME, "Key": filekey},
        )
    except ClientError as e:
        return {'url': '', 'error': e}

    return {'url': presigned_url.split('?')[0], 'error': None}

def fileobj2url(fileobj, filekey):
    s3_client = init_client()
    try:
        s3_client.upload_fileobj(fileobj, STORAGE_NAME, filekey)

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": STORAGE_NAME, "Key": filekey},
        )
    except ClientError as e:
        return {'url': '', 'error': e}

    return {'url': presigned_url.split('?')[0], 'error': None}
