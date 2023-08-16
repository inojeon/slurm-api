from app.db.models import (
    UploadInputfile,
    CreateInputfile,
    LoadFileList,
    LoadFile,
    FileTypeAndName,
)
import os, string, random
from app.db.config import REPO_DIR, JOBS_DIR


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def write_file(file_path: str, content: str) -> bool:
    if os.path.exists(file_path):
        file_name = file_path.split(".")[0]
        file_exe = file_path.split(".")[1]
        file_path = f"{file_name}-{id_generator()}.{file_exe}"

    f = open(file_path, "w")
    f.write(content)
    f.close()

    return True


def create_inputfile(item: UploadInputfile) -> CreateInputfile:
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
    file_path = f"{REPO_DIR}/{item.name}"

    if write_file(file_path, item.content):
        return CreateInputfile(ok=True, filePath=file_path)
    else:
        return CreateInputfile(ok=False)


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


def read_resultfiles(jobId: str):
    from app.libs.jobs import find_jobName

    jobName = find_jobName(int(jobId))
    return LoadFileList(
        ok=True, fileLists=read_files(f"{JOBS_DIR}/{jobName}"), filePath=JOBS_DIR
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


def read_resultfile(jobId: str, resultfileName: str) -> LoadFile:
    from app.libs.jobs import find_jobName

    jobName = find_jobName(int(jobId))
    resultfile_path = f"{JOBS_DIR}/{jobName}/{resultfileName}"
    return read_file(resultfile_path)
