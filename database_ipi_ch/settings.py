from scrapers_shared.shared_settings import SharedSettings
from minio import Minio
from minio.error import S3Error


class Settings(SharedSettings):
    page_size: int = 64
    output_file: str = "./output.jsonl"
    last_cursor_file: str = "./last_cursor.json"
    folder_name: str = "database_ipi_ch"
    bucket: str = "marc-testing2"

    def upload_to_minio(self, s3_endpoint, s3_access_key, s3_secret_key, bucket):
        client = Minio(
            s3_endpoint,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
        )

        # Make 'asiatrip' bucket if not exist.
        found = client.bucket_exists(bucket)
        if not found:
            client.make_bucket(bucket)
        else:
            print(f"Bucket {bucket} already exists")

        # Upload '/home/user/Photos/asiaphotos.zip' as object name
        # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
        destination = "database_ipi_ichi/output.jsonl"

        file = "output.jsonl"
        client.fput_object(
            bucket,
            destination,
            file,
        )
        print(
            f"'{destination}' is successfully uploaded as "
            f"object '{file}' to bucket '{bucket}'."
        )
