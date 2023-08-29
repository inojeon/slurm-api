from typing import Union

from app.db.models import ProgramDetail, Programs, SubmitJob, UploadInputfile
from app.libs.files import create_inputfile
import json, os


def load_programs() -> Union[Programs, None]:
    PROGRAM_DB_PATH = f"{os.getcwd()}/src/app/db/programs.json"

    with open(PROGRAM_DB_PATH, "r") as file:
        return json.load(file)


def load_program_info(programName: str) -> Union[ProgramDetail, None]:
    PROGRAM_DB_PATH = f"{os.getcwd()}/src/app/db/programs.json"

    with open(PROGRAM_DB_PATH, "r") as file:
        programs = json.load(file)

    for program in programs:
        if program["name"] == programName:
            detail_info_path = f"{program['location']}/{program['infoJsonPath']}"
            if not os.path.exists(detail_info_path):
                return None
            with open(detail_info_path, "r") as file:
                return ProgramDetail(**json.load(file))
    return None


def creat_job_script(program: ProgramDetail, jobInfo: SubmitJob) -> Union[str, None]:
    # add slurm options
    script = "#!/bin/bash\n"
    script += f"#SBATCH --job-name={jobInfo.jobName}\n"
    script += f"#SBATCH --nodes={program.slurm.nodes}\n"
    script += "#SBATCH -e std.err\n"
    script += "#SBATCH -o std.out\n"
    script += "\n"
    if program.preScript:
        script += f"{program.preScript}\n"
    # if program.shell == "python3":

    script += f"export PROGRAM_HOME={program.location}\n\n"

    script += f"{program.shell} {program.location}/{program.mainExe} "

    for inputFile in jobInfo.inputFiles:
        script += f"{inputFile.option} {inputFile.path} "
    if jobInfo.inputParameter:
        newInpFileInfo = UploadInputfile(
            name=f"{jobInfo.jobName.replace(' ', '-')}.inp",
            content=jobInfo.inputParameter,
        )
        inpFileGenResult = create_inputfile(newInpFileInfo)
        if inpFileGenResult.ok:
            script += f"--inp {inpFileGenResult.filePath} "
    script += "\n\n"
    if program.postSrcipt:
        script += program.postSrcipt
    script += "\n"

    return script
