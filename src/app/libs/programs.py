from typing import Union

from app.db.models import ProgramDetail, Programs
import json, os


def load_programs() -> Union[Programs, None]:
    PROGRAM_DB_PATH = f"{os.getcwd()}/app/db/programs.json"

    with open(PROGRAM_DB_PATH, "r") as file:
        return json.load(file)


def load_program_info(programName: str) -> Union[ProgramDetail, None]:
    PROGRAM_DB_PATH = f"{os.getcwd()}/app/db/programs.json"

    with open(PROGRAM_DB_PATH, "r") as file:
        programs = json.load(file)

    for program in programs:
        if program["name"] == programName:
            detail_info_path = f"{program['location']}/{program['infoJsonPath']}"
            if not os.path.exists(detail_info_path):
                return None
            with open(detail_info_path, "r") as file:
                return json.load(file)
    return None
