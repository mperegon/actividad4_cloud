from fastapi import APIRouter, Body, HTTPException, Header, File, UploadFile
from pydantic import BaseModel
from typing import List
from ..dependency_injection.container import FilesContainer
from ..domain.business_objects import FileCreation, MergeRequest
from ..domain.exceptions import (
    FileNotFoundException,
    UnauthorizedFileAccessException,
    FileStorageException,
    MergeException
)
from app.authentication.dependency_injection.container import AuthenticationContainer

router = APIRouter()

file_storage_service = FileStoragePersistences.carlemany()


class FileInfoInput(BaseModel):
    title: str
    author: str
    year: int
    filename: str

class FileInfoOutput(BaseModel):
    id: int
    title: str
    author: str
    year: int
    filename: str
    owner_external_id: int

class MergeInput(BaseModel):
    file_ids: List[int]
    title: str
    filename: str


async def get_current_user_external_id(auth: str) -> int:
    auth_container = AuthenticationContainer()
    introspect_controller = auth_container.get_introspect_controller()

    user = await introspect_controller.verify_token(auth)
    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")

    return user.external_id

@router.get("", response_model=List[FileInfoOutput])
async def files_get(auth: str = Header(alias="Auth")) -> List[FileInfoOutput]:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        files = await files_service.get_files_by_user(owner_external_id)
        return [
            FileInfoOutput(
                id=file.id,
                title=file.title,
                author=file.author,
                year=file.year,
                filename=file.filename,
                owner_external_id=file.owner_external_id
            )
            for file in files
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=FileInfoOutput)
async def files_post(input: FileInfoInput = Body(), auth: str = Header(alias="Auth")) -> FileInfoOutput:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        file_data = FileCreation(
            title=input.title,
            author=input.author,
            year=input.year,
            filename=input.filename
        )

        file_info = await files_service.create_file(file_data, owner_external_id)

        return FileInfoOutput(
            id=file_info.id,
            title=file_info.title,
            author=file_info.author,
            year=file_info.year,
            filename=file_info.filename,
            owner_external_id=file_info.owner_external_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=FileInfoOutput)
async def files_id_get(id: int, auth: str = Header(alias="Auth")) -> FileInfoOutput:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        file_info = await files_service.get_file_by_id(id, owner_external_id)

        return FileInfoOutput(
            id=file_info.id,
            title=file_info.title,
            author=file_info.author,
            year=file_info.year,
            filename=file_info.filename,
            owner_external_id=file_info.owner_external_id
        )
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def files_id_delete(id: int, auth: str = Header(alias="Auth")) -> dict[str, str]:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        await files_service.delete_file(id, owner_external_id)
        return {"status": "deleted"}
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{id}")
async def files_id_post(id: int, file: UploadFile = File(), auth: str = Header(alias="Auth")) -> dict[str, str]:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        content = await file.read()
        await files_service.upload_file_content(id, content, file.filename, owner_external_id)
        return {"status": "uploaded"}
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden")
    except FileStorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/merge", response_model=FileInfoOutput)
async def files_merge_post(input: MergeInput = Body(), auth: str = Header(alias="Auth")) -> FileInfoOutput:
    owner_external_id = await get_current_user_external_id(auth)

    container = FilesContainer()
    files_service = container.get_files_service()

    try:
        merge_request = MergeRequest(
            file_ids=input.file_ids,
            title=input.title,
            filename=input.filename
        )

        merged_file = await files_service.merge_pdf_files(merge_request, owner_external_id)

        return FileInfoOutput(
            id=merged_file.id,
            title=merged_file.title,
            author=merged_file.author,
            year=merged_file.year,
            filename=merged_file.filename,
            owner_external_id=merged_file.owner_external_id
        )
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorizedFileAccessException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except MergeException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))