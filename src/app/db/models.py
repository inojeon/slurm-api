from pydantic import BaseModel


class UploadInputfile(BaseModel):
    name: str
    content: str
