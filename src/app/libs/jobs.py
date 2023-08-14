from app.db.models import SubmitJob, CreatJob

from app.libs.programs import load_program_info, creat_job_script
from app.db.config import JOBS_DIR
from app.libs.files import id_generator, write_file
import os


def create_job_dir(jobName: str) -> str:
    job_dir_path = f"{JOBS_DIR}/{jobName.replace(' ','-')}"

    if os.path.exists(job_dir_path):
        job_dir_path += f"-{id_generator(4)}"
    os.makedirs(job_dir_path)

    return job_dir_path


def create_job(jobInfo: SubmitJob) -> CreatJob:
    program = load_program_info(jobInfo.programName)
    if not program:
        return CreatJob(ok=False)

    job_dir_path = create_job_dir(jobInfo.jobName)

    print(job_dir_path)

    script_template = creat_job_script(program, jobInfo)
    print(script_template)

    batch_script_path = f"{job_dir_path}/batch.sh"
    write_file(batch_script_path, script_template)

    os.chdir(job_dir_path)
    # os.system("sbatch s")
    return_value = os.popen("sbatch batch.sh").read()

    slurmJobId = int(return_value.split("Submitted batch job ")[1])

    print(slurmJobId)

    return CreatJob(ok=True, slurmJobId=slurmJobId)
