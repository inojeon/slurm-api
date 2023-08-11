from typing import List
from pydantic import BaseModel


class UploadInputfile(BaseModel):
    name: str
    content: str


class InputFile(BaseModel):
    type: str
    path: str


class SubmitJob(BaseModel):
    programName: str
    inputFiles: List[InputFile]
    inputParameter: str
