from app.db.models import UploadInputfile
import os, string, random

USER_PROJECT_DIR = "/home/admin"
REPO_DIR = f"{USER_PROJECT_DIR}/repository"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_inputfile(item: UploadInputfile):
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

    return {"ok": True, "filePath": file_path}


def read_inputfiles():
    return {"ok": True, "filePath": REPO_DIR, "fileLists": os.listdir(REPO_DIR)}


def read_inputfile(inputfileName: str):
    inputfile_path = f"{REPO_DIR}/{inputfileName}"
    # print(os.path.exists(inputfile_path))
    if not os.path.exists(inputfile_path):
        return {"ok": False, "message": "file doesn't exist"}

    f = open(inputfile_path, "r")
    file_content = f.read()
    f.close()
    return {
        "ok": True,
        "filePath": inputfile_path,
        "content": file_content,
    }
