from fastapi import HTTPException, status, APIRouter
from typing import Union

# from src.libs.files import create_inputfile
from app.db.models import SubmitJob
from app.libs.jobs import create_job


router = APIRouter()


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def submit_job(item: SubmitJob):
    return create_job(item)
