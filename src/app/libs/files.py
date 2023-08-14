from app.db.models import (
    UploadInputfile,
    CreateInputfile,
    LoadFileList,
    LoadFile,
    FileTypeAndName,
)
import os, string, random

USER_PROJECT_DIR = "/home/admin"
REPO_DIR = f"{USER_PROJECT_DIR}/repository"
JOBS_DIR = f"{USER_PROJECT_DIR}/jobs"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_inputfile(item: UploadInputfile) -> CreateInputfile:
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
    file_path = f"{REPO_DIR}/{item.name}"

    if os.path.exists(file_path):
        file_name = file_path.split(".")[0]
        file_exe = file_path.split(".")[1]
        file_path = f"{file_name}-{id_generator()}.{file_exe}"

    f = open(file_path, "w")
    f.write(item.content)
    f.close()

    return CreateInputfile(ok=True, filePath=file_path)


def read_files(path: str) -> [FileTypeAndName]:
    result = []
    for file in os.listdir(path):
        d = os.path.join(path, file)
        if os.path.isdir(d):
            result.append(FileTypeAndName(name=file, type="dir"))
        else:
            result.append(FileTypeAndName(name=file, type="file"))
    return result


def read_inputfiles():
    return LoadFileList(ok=True, fileLists=read_files(REPO_DIR), filePath=REPO_DIR)


def read_resultfiles(jobID: str):
    return LoadFileList(
        ok=True, fileLists=read_files(f"{JOBS_DIR}/{jobID}"), filePath=REPO_DIR
    )


def read_file(filePath: str) -> LoadFile:
    if not os.path.exists(filePath):
        return LoadFile(ok=False, message="file doesn't exist")

    f = open(filePath, "r")
    fileContent = f.read()
    f.close()

    return LoadFile(ok=True, filePath=filePath, content=fileContent)


def read_inputfile(inputfileName: str) -> LoadFile:
    inputfile_path = f"{REPO_DIR}/{inputfileName}"
    return read_file(inputfile_path)


def read_resultfile(resultfileName: str, jobID: str) -> LoadFile:
    resultfile_path = f"{JOBS_DIR}/{jobID}/{resultfileName}"
    return read_file(resultfile_path)
