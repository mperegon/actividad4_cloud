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

    def put_file(self, local_path: str, remote_identifier: str):
        self.minio_client.fput_object(
            self.bucket_name, 
            object_name=remote_identifier,
            file_path=local_path,   
        )
        return f"localhost:¨{minio_settings.port}/{self.bucket_name}/{remote_identifier}"
    
    def get_file(self, remote_path: str, local_folder: str):
        remote_identifier = remote_path.split("/")[-1]
        local_path= f"{local_folder}/{remote_identifier}"
        self.minio_client.fget_object(
            self.bucket_name,
            remote_identifier,
            f"{local_folder}/{remote_identifier}"
        )
        return local_path