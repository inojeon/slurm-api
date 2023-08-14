from typing import List, Union
from pydantic import BaseModel


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
    preScript: str
    postSrcipt: str
    slurm: Slurm
    shell: str
    mainExe: str
    inputs: List[Input]
    required: Required
