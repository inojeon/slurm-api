from app.db.models import UploadInputfile
import os

USER_PROJECT_DIR = "/home/admin"
REPO_DIR = f"{USER_PROJECT_DIR}/repository"


def create_input_file(item: UploadInputfile):
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
    file_path = f"{REPO_DIR}/{item.name}"

    if os.path.exists(file_path):
        return {"ok": False, "message": "file name duplicated"}

    f = open(file_path, "w")
    f.write(item.content)
    f.close()

    return {"ok": True, "filePath": file_path}
