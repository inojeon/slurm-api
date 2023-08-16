# main.py
from fastapi import FastAPI
from app.api import files, jobs, programs

from app.libs.jobs import save_fake_db_to_json

app = FastAPI()


@app.get("/")
def read_root():
    return {"title": "Slurm API Server POC"}


@app.on_event("shutdown")  # new
async def app_shutdown():
    save_fake_db_to_json()


app.include_router(files.router)
app.include_router(jobs.router)
app.include_router(programs.router)
