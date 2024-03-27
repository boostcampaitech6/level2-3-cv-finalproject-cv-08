from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("MINIO_BUCKET")
MINIO_API_HOST = os.getenv("MINIO_ENDPOINT")