from fastapi import status, APIRouter

from app.libs.programs import load_programs, load_program_info


router = APIRouter()


@router.get("/programs", status_code=status.HTTP_200_OK)
async def get_read_programs():
    return load_programs()


@router.get("/program/{program_name}", status_code=status.HTTP_200_OK)
async def get_read_program_name(program_name: str):
    return load_program_info(program_name)
