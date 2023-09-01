import os, json
from typing import Union
from fastapi.encoders import jsonable_encoder

from app.db.models import SubmitJob, CreatJob, JobInfoDB, JobInfoDBTable
from app.db.config import JOBS_DIR

from app.libs.programs import load_program_info, creat_job_script
from app.libs.files import id_generator, write_file

JOBS_DB_PATH = f"{os.getcwd()}/app/db/jobs.json"

fake_job_db: JobInfoDBTable = []

if os.path.exists(JOBS_DB_PATH):
    with open(JOBS_DB_PATH, "r") as file:
        json_datas = json.load(file)
        for data in json_datas:
            fake_job_db.append(JobInfoDB(**data))


def get_job_unique_jobname(jobName: str) -> str:
    job_dir_path = f"{JOBS_DIR}/{jobName.replace(' ','-')}"

    if os.path.exists(job_dir_path):
        return f"{jobName}-{id_generator(4)}"
    else:
        return jobName


def create_job_dir(jobName: str) -> str:
    job_dir_path = f"{JOBS_DIR}/{jobName.replace(' ','-')}"

    if os.path.exists(job_dir_path):
        job_dir_path += f"-{id_generator(4)}"
    os.makedirs(job_dir_path)

    return job_dir_path


def insert_job_into_fake_db(newJob: JobInfoDB) -> bool:
    fake_job_db.append(newJob)
    return True


def read_jobs_info_fake_db(limit: int = 5):
    return fake_job_db[len(fake_job_db) - limit : :][::-1]
    # print(fake_job_db)
    # return fake_job_db


def get_jobId_into_jobName(jobName: str):
    for job in fake_job_db:
        if job.jobName == jobName:
            return job.jobId


def read_detail_job_unfo_fake_db(jobName: str):
    jobId = get_jobId_into_jobName(jobName)
    update_job_status(jobId)
    for job in fake_job_db:
        if job.jobId == jobId:
            return job
    return None


def read_job_info_fake_db(jobId: int) -> Union[JobInfoDB, None]:
    update_job_status(jobId)
    for job in fake_job_db:
        if job.jobId == jobId:
            return job
    return None


def save_fake_db_to_json() -> bool:
    with open(JOBS_DB_PATH, "w") as file:
        file.write(json.dumps(jsonable_encoder(fake_job_db), indent=2))


def find_jobName(jobId: int):
    for job in fake_job_db:
        if job.jobId == jobId:
            return job.jobName
    return None


def find_job_dir(jobId: int):
    for job in fake_job_db:
        if job.jobId == jobId:
            return job.jobDir
    return None


def check_job_status(jobId: int):
    for job in fake_job_db:
        if job.jobId == jobId:
            return job.status
    return None


def update_job_status(jobId: int):
    scontrol_result = (
        os.popen(f"scontrol show job {jobId} | grep JobState").read().strip()
    )

    if len(scontrol_result) == 0:
        return False

    job_status = scontrol_result.split(" ")[0].split("JobState=")[1]

    for index, item in enumerate(fake_job_db):
        if item.jobId == jobId:
            if fake_job_db[index].status != job_status:
                fake_job_db[index].status = job_status

    return True


def create_job(jobInfo: SubmitJob) -> CreatJob:
    program = load_program_info(jobInfo.programName)
    if not program:
        return CreatJob(ok=False)

    jobName = get_job_unique_jobname(jobInfo.jobName)
    # create job Dir
    job_dir_path = create_job_dir(jobName)

    # Create slurm job script
    script_template = creat_job_script(program, jobInfo)

    # Save job script /{jobDir}/batch.sh
    batch_script_path = f"{job_dir_path}/batch.sh"
    write_file(batch_script_path, script_template)

    root_dir = os.getcwd()
    # run slurm sbatch
    os.chdir(job_dir_path)
    return_value = os.popen("sbatch batch.sh").read()
    os.chdir(root_dir)

    # get slurm jobID
    slurmJobId = int(return_value.split("Submitted batch job ")[1])

    # slurmJobId = 11
    newJob = JobInfoDB(
        jobName=jobName, jobDir=job_dir_path, status="PENDING", jobId=slurmJobId
    )

    saveResult = insert_job_into_fake_db(newJob)

    print(saveResult)

    return CreatJob(ok=True, slurmJobId=slurmJobId, jobName=jobName)


def update_log_data(jobId: int, endline: int = 1):
    JOB_LOG_PATH = f"{find_job_dir(int(jobId))}/std.out"
    total_len = sum(1 for _ in open(JOB_LOG_PATH))
    if total_len == endline:
        scontrol_result = (
            os.popen(f"scontrol show job {jobId} | grep JobState").read().strip()
        )
        job_status = scontrol_result.split(" ")[0].split("JobState=")[1]

        if job_status == "RUNNING":
            return {"ok": True, "endline": total_len, "datas": None}
        else:
            return {"ok": False}

    result = ""
    with open(JOB_LOG_PATH, "r") as file:
        for line in file.readlines()[endline:]:
            result += line.replace("\n", "</br>")
        return {"ok": True, "endline": total_len, "datas": result}
