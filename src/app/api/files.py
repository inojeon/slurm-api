from fastapi import HTTPException, status, APIRouter
from typing import Union

from app.db.models import UploadInputfile
from app.libs.files import (
    create_inputfile,
    read_inputfiles,
    read_inputfile,
    read_resultfiles,
    read_resultfile,
)

router = APIRouter()


@router.post("/inputfiles", status_code=status.HTTP_201_CREATED)
async def create_upload_file(item: Union[UploadInputfile, None] = None):
    return create_inputfile(item)


@router.get("/inputfiles", status_code=status.HTTP_200_OK)
async def read_input_files():
    result = read_inputfiles()
    if not result.ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    return result


@router.get("/inputfiles/{inputfileName}", status_code=status.HTTP_200_OK)
async def read_input_file(inputfileName: str):
    result = read_inputfile(inputfileName)
    if not result.ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    return result


@router.get("/resultfiles/{jobId}", status_code=status.HTTP_200_OK)
async def get_read_result_files(jobId: str):
    result = read_resultfiles(jobId)
    if not result.ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    return result


@router.get("/resultfiles/{jobId}/{resultfileName}", status_code=status.HTTP_200_OK)
async def get_read_result_file(jobId: str, resultfileName: str):
    result = read_resultfile(jobId, resultfileName)
    if not result.ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    return result
