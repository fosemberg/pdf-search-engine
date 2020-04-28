from botocore.client import Config
import boto3

ENDPOINT = "https://storage.yandexcloud.net"
ACCESS_KEY = "Kh_5cDVkTRoSHivFUvUA"
SECRET_KEY = "1VFz0tGxlDbEUxF4CtL29LE-JSuN5eyFfIfEWMM8"
STORAGE_NAME = "pdf-storage"

def file2url(filename, filekey):
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

    s3.upload_file(filename, STORAGE_NAME, filekey)

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": STORAGE_NAME, "Key": filekey},
        ExpiresIn=100,
    )

    return presigned_url

def fileobj2url(fileobj, filekey):
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

    s3.upload_fileobj(fileobj, STORAGE_NAME, filekey)

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": STORAGE_NAME, "Key": filekey},
        ExpiresIn=100,
    )

    return presigned_url
