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
                owner_external_id=file.owner_external_id,
                url=current.file_path
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
    public_path = file_storage_service.put_file()

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

    return {"path":public_path}

@router.post("/merge")
async def files_id_post(auth:str =Header(), input: FilesMMergeInput = Body())
    introspect_user = await introspect(token=auth)
    file_1= check_file_ownership(id=input.file_id_1, user=introspect_user)
    file_2= check_file_ownership(id=input.file_id_2, user=introspect_user)
    file_1_path=file_1.path
    file_2_path=file_2.path

    if file_1_path is None or file_2_path is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    file_1_local_path = file_storage_service.get_file(file_1_path, "files")
    file_2_local_path = file_storage_service.get_file(file_2_path, "files")



    file_1_name = file_1_path.split("/")[-1].split(".")[0]
    file_2_name = file_2_path.split("/")[-1].split(".")[0]
    pdfs = [file_1_local_path,file_2_local_path]
    filename =f"{file_1_name}_{file_2_name}.pdf"

    merged_path = f"files/{filename}"
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(merged_path)
    merger.close()
    remote_merged_pathfile_storage_service.put_file(merged_path, filename)
    os.remove(merged_path)
    return {"path:"remote_merged_path}
