from app.db.models import SubmitJob

from app.libs.programs import load_program_info


def create_job(item: SubmitJob):
    program = load_program_info(item.programName)
    if not program:
        return {"ok": False}
    print(program)
    # program_detail_info = load_program_template(
    #     f"{program['location']}/{program['infoJsonPath']}"
    # )
    # print(program_detail_info)
    return {"ok": True}
