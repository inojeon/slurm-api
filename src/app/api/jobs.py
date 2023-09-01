from fastapi import status, APIRouter, WebSocket, Request, HTTPException
from fastapi.templating import Jinja2Templates

from app.db.models import SubmitJob
from app.libs.jobs import (
    create_job,
    read_job_info_fake_db,
    update_log_data,
    read_jobs_info_fake_db,
    read_detail_job_unfo_fake_db,
)

import asyncio
from pathlib import Path

router = APIRouter()

# set path and log file name
base_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(base_dir, "templates")))


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def submit_job(item: SubmitJob):
    return create_job(item)


@router.get("/jobs")
async def get_jobs(limit: int = 5):
    return read_jobs_info_fake_db(int(limit))


@router.get("/detailjob/{jobName}", status_code=status.HTTP_200_OK)
async def get_job_detail_info(jobName: str):
    return read_detail_job_unfo_fake_db(jobName)


@router.get("/jobs/{jobId}", status_code=status.HTTP_200_OK)
async def get_job_info(jobId: str):
    result = read_job_info_fake_db(int(jobId))
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.get("/logtest")
async def get_log_test_page(request: Request):
    """Log file viewer

    Args:
        request (Request): Default web request.

    Returns:
        TemplateResponse: Jinja template with context data.
    """
    context = {
        "title": "FastAPI Streaming Log Viewer over WebSockets",
        "log_file": "std.out",
    }
    return templates.TemplateResponse(
        "index.html", {"request": request, "context": context}
    )


@router.websocket("/ws/log/{jobId}")
async def websocket_endpoint_log(websocket: WebSocket, jobId: str) -> None:
    """WebSocket endpoint for client connections

    Args:
        websocket (WebSocket): WebSocket request from client.
    """
    await websocket.accept()
    endline = 0
    try:
        while True:
            await asyncio.sleep(1)
            resultlogs = update_log_data(jobId, endline)
            endline = resultlogs["endline"]
            print(endline)
            if resultlogs["ok"] and resultlogs["datas"]:
                await websocket.send_text(resultlogs["datas"])
    except Exception as e:
        print(e)
    finally:
        await websocket.close()
