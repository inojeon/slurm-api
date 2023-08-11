# main.py
from fastapi import FastAPI
from app.api import files, jobs

app = FastAPI()


@app.get("/")
def read_root():
    return {"title": "Slurm API Server POC"}


app.include_router(files.router)
app.include_router(jobs.router)
