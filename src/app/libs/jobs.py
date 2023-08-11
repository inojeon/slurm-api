from app.db.models import SubmitJob


def create_job(item: SubmitJob):
    return {"ok": True}
