from dependency_injector import containers, providers
from app.files.persistece.minio.minio_file_storage_service import MinioFileStorageService

class FileStoragePersistences(containers.DeclarativeContainer):
    minio = providers.Singleton(
        MinioFileStorageService
    )

    carlemany = minio

