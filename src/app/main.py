# main.py
from fastapi import FastAPI, HTTPException, status
from typing import Union

# from src.libs.files import create_input_file
from app.db.models import UploadInputfile
from app.libs.files import create_input_file


app = FastAPI()


@app.get("/")
def read_root():
    return {"title": "Slurm API Server POC"}


@app.post("/inputfiles", status_code=status.HTTP_201_CREATED)
async def create_upload_file(item: Union[UploadInputfile, None] = None):
    create_result = create_input_file(item)

    print(create_result)
    if create_result.get("ok") is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=create_result.get("message"),
        )

    return create_result
