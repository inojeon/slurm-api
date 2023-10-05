from typing import List, Union, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class CreateInputfile(BaseModel):
    ok: bool
    filePath: Optional[str]


class FileTypeEnum(str, Enum):
    dir = "dir"
    file = "file"


class FileTypeAndName(BaseModel):
    type: FileTypeEnum
    name: str


class LoadFileList(BaseModel):
    ok: bool
    filePath: Optional[str] = None
    fileLists: Optional[List[FileTypeAndName]] = None
    message: Optional[str] = None


class LoadFile(BaseModel):
    ok: bool
    filePath: Optional[str] = None
    content: Optional[str] = None
    message: Optional[str] = None


class JobInfoDB(BaseModel):
    jobName: str
    jobId: int
    status: str
    jobDir: str
    startDate: Optional[datetime] = datetime.today()
    endDate: Optional[datetime] = None


class JobInfoDBTable(BaseModel):
    List[Union[JobInfoDB, None]]
    # List(Union[JobInfoDB, None])


class CreateJob(BaseModel):
    ok: bool
    slurmJobId: Optional[int] = None
    jabName: Optional[str] = None


class UploadInputfile(BaseModel):
    name: str
    content: str


class InputFile(BaseModel):
    option: str
    path: str


class SubmitJob(BaseModel):
    programName: str
    inputFiles: List[InputFile]
    inputParameter: Union[str, None]
    jobName: str
    jobDescription: Union[str, None]
    isParallel: bool = False


class Program(BaseModel):
    name: str
    location: str
    settingPath: str


class Programs(BaseModel):
    List[Program]


class SampleInputItem(BaseModel):
    option: str
    path: str


class Slurm(BaseModel):
    runType: str
    nodes: int


class Input(BaseModel):
    option: str
    exec: str
    sampleInputPath: str


class Required(BaseModel):
    environ: List[str]


class ProgramDetail(BaseModel):
    name: str
    version: str
    location: str
    runScript: str
    slurm: Slurm
    inputs: List[Input]
