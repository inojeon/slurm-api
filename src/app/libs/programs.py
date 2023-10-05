from typing import Union

from app.db.models import ProgramDetail, Programs, SubmitJob, UploadInputfile
from app.libs.files import create_inputfile
import json, os, toml

PROGRAM_DB_PATH = f"{os.getcwd()}/app/db/programs.json"


def load_programs() -> Union[Programs, None]:
    with open(PROGRAM_DB_PATH, "r") as file:
        return json.load(file)


def load_program_inputschema(programName: str) -> Union[object, None]:
    with open(PROGRAM_DB_PATH, "r") as file:
        programs = json.load(file)

    for program in programs:
        if program["name"] == programName:
            detail_info_path = f"{program['location']}/{program['inputSchemaPath']}"
            if not os.path.exists(detail_info_path):
                return None
            with open(detail_info_path, "r") as file:
                return json.load(file)
    return None


def load_program_sampleinput(programName: str) -> Union[object, None]:
    with open(PROGRAM_DB_PATH, "r") as file:
        programs = json.load(file)

    for program in programs:
        if program["name"] == programName:
            sampleinputPath = f"{program['location']}/{program['inputSamplePath']}"
            if not os.path.exists(sampleinputPath):
                return None
            with open(sampleinputPath, "r") as file:
                return toml.loads(file.read())
    return None


def load_program_info(programName: str) -> Union[ProgramDetail, None]:
    with open(PROGRAM_DB_PATH, "r") as file:
        programs = json.load(file)

    for program in programs:
        if program["name"] == programName:
            detail_info_path = f"{program['location']}/{program['settingPath']}"
            if not os.path.exists(detail_info_path):
                return None
            with open(detail_info_path, "r") as file:
                import yaml

                data = yaml.load(file.read(), Loader=yaml.Loader)
                print(data)
                return ProgramDetail(**data)
    return None


def creat_job_script(program: ProgramDetail, jobInfo: SubmitJob) -> Union[str, None]:
    # add slurm options
    script = "#!/bin/bash\n"
    script += f"#SBATCH --job-name={jobInfo.jobName}\n"
    script += f"#SBATCH --nodes={program.slurm.nodes}\n"
    script += "#SBATCH -e std.err\n"
    script += "#SBATCH -o std.out\n"
    script += "\n"

    inputStr = ""

    for inputFile in jobInfo.inputFiles:
        inputStr += f"{inputFile.option} {inputFile.path} "
    if jobInfo.inputParameter:
        newInpFileInfo = UploadInputfile(
            name=f"{jobInfo.jobName.replace(' ', '-')}.inp",
            content=jobInfo.inputParameter,
        )
        inpFileGenResult = create_inputfile(newInpFileInfo)
        if inpFileGenResult.ok:
            inputStr += f"--inp {inpFileGenResult.filePath} "

    tmpScript = program.runScript

    tmpScript = tmpScript.replace("&&PROGRAM_HOME&&", program.location)
    tmpScript = tmpScript.replace("&&inputArgs&&", inputStr)
    script += tmpScript

    return script
