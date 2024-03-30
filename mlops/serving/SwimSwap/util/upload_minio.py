import os
from minio import Minio

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

def upload_object(client, filename, data, length, BUCKET_NAME,content_type=None):

    # Make bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket {BUCKET_NAME} already exists")
    if content_type is not None:
        client.put_object(BUCKET_NAME, filename, data, length,content_type=content_type)
    else:
        client.put_object(BUCKET_NAME, filename, data, length)
    print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")