import io
from google.cloud import storage

class FileStorage:
    def __init__(self, bucket_name) -> None:
        self.bucket_name = bucket_name

    def get_file(self, filename):
        """Downloads a blob into memory."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        string_buffer = io.BytesIO()
        blob.download_to_file(string_buffer)
        return string_buffer.getvalue()

    def save_file_from_file(self, filename, content):
        """Write and read a blob from GCS using file-like IO"""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_file(content)

    def save_file(self, filename, content):
        """Write and read a blob from GCS using file-like IO"""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(content)

    def delete_file(self, filename):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()

        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        blob.delete()