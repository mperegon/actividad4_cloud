from app.files.domain.persistences.file_storage_interface import FileStorageInterface
from app.config import minio_settings
from minio import Minio

class MinioFileStorageService(FileStorageInterface):
    
    def __init__(self):
        self.minio_client = Minio(
            f"${minio_settings.host}:{minio_settings.port}",
            access_key=minio_settings.root_user,
            secret_key=minio_settings.root_password,
            secure=False
        )
        self.buket_name=minio_settings.bucket_name