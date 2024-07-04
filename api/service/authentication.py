import google.auth
from google.cloud import storage

class Authentication:
    def __init__(self, credential_key, bucket_name):
        credentials, _ = google.auth.load_credentials_from_file(
        credential_key
        )
        self.credentials = credentials
        self.storage_client = storage.Client(credentials=credentials)
        bucket = self.storage_client.bucket(bucket_name)
        self.bucket_name = bucket_name
        self.bucket = bucket

    def get_bucket(self):
        return self.bucket

    def get_bucket_name(self):
        return self.bucket_name

    def get_translate_client(self):
        return self.translate_client