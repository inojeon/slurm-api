from app.db.models import SubmitJob

from app.libs.programs import load_program_info, creat_job_script


def create_job(jobInfo: SubmitJob):
    program = load_program_info(jobInfo.programName)
    if not program:
        return {"ok": False}

    script_template = creat_job_script(program, jobInfo)
    print(script_template)
    return {"ok": True}
