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
    message: Optional[float] = None


class LoadFile(BaseModel):
    ok: bool
    filePath: Optional[str] = None
    content: Optional[str] = None
    message: Optional[float] = None


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


class CreatJob(BaseModel):
    ok: bool
    slurmJobId: Union[int, None]


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
    infoJsonPath: str


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


class Required(BaseModel):
    environ: List[str]


class ProgramDetail(BaseModel):
    name: str
    version: str
    sampleInput: List[SampleInputItem]
    location: str
    preScript: str
    postSrcipt: str
    slurm: Slurm
    shell: str
    mainExe: str
    inputs: List[Input]
    required: Required
