from fastapi import status, APIRouter

from app.db.models import SubmitJob
from app.libs.jobs import create_job


router = APIRouter()


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def submit_job(item: SubmitJob):
    return create_job(item)
