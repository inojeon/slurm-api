from app.db.models import SubmitJob, CreatJob, JobInfoDB, JobInfoDBTable

from app.libs.programs import load_program_info, creat_job_script
from app.db.config import JOBS_DIR
from app.libs.files import id_generator, write_file
import os
from fastapi.encoders import jsonable_encoder


def create_job_dir(jobName: str) -> str:
    job_dir_path = f"{JOBS_DIR}/{jobName.replace(' ','-')}"

    if os.path.exists(job_dir_path):
        job_dir_path += f"-{id_generator(4)}"
    os.makedirs(job_dir_path)

    return job_dir_path


def insert_job_into_json_db(newJob: JobInfoDB) -> bool:
    import json

    JOBS_DB_PATH = f"{os.getcwd()}/app/db/jobs.json"

    if os.path.exists(JOBS_DB_PATH):
        with open(JOBS_DB_PATH, "r") as file:
            jsonData = json.load(file)
    else:
        jsonData: JobInfoDBTable = []
    jsonData.append(newJob)

    with open(JOBS_DB_PATH, "w") as file:
        file.write(json.dumps(jsonable_encoder(jsonData), indent=2))

    return True


def create_job(jobInfo: SubmitJob) -> CreatJob:
    program = load_program_info(jobInfo.programName)
    if not program:
        return CreatJob(ok=False)

    # create job Dir
    job_dir_path = create_job_dir(jobInfo.jobName)

    # Create slurm job script
    script_template = creat_job_script(program, jobInfo)

    # Save job script /{jobDir}/batch.sh
    batch_script_path = f"{job_dir_path}/batch.sh"
    write_file(batch_script_path, script_template)

    # root_dir = os.getcwd()
    # run slurm sbatch
    # os.chdir(job_dir_path)
    # return_value = os.popen("sbatch batch.sh").read()
    # os.chdir(root_dir)

    # get slurm jobID
    # slurmJobId = int(return_value.split("Submitted batch job ")[1])

    slurmJobId = 11
    newJob = JobInfoDB(
        jobName=jobInfo.jobName, jobDir=job_dir_path, status="PENDING", jobId=slurmJobId
    )

    saveResult = insert_job_into_json_db(newJob)

    print(saveResult)

    return CreatJob(ok=True, slurmJobId=slurmJobId)
