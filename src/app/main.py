# main.py
from fastapi import FastAPI, HTTPException, status
from typing import Union

# from src.libs.files import create_inputfile
from app.db.models import UploadInputfile
from app.libs.files import create_inputfile, read_inputfiles, read_inputfile


app = FastAPI()


@app.get("/")
def read_root():
    return {"title": "Slurm API Server POC"}


@app.post("/inputfiles", status_code=status.HTTP_201_CREATED)
async def create_upload_file(item: Union[UploadInputfile, None] = None):
    return create_inputfile(item)


@app.get("/inputfiles", status_code=status.HTTP_200_OK)
async def read_input_files():
    return read_inputfiles()


@app.get("/inputfiles/{inputfileName}", status_code=status.HTTP_200_OK)
async def read_input_file(inputfileName: str):
    result = read_inputfile(inputfileName)
    print(result)
    if not result.get("ok"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.get("message")
        )
    return result
