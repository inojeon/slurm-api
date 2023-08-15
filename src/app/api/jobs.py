from fastapi import status, APIRouter, WebSocket, Request
from fastapi.templating import Jinja2Templates

from app.db.models import SubmitJob
from app.libs.jobs import create_job

import asyncio
from pathlib import Path

router = APIRouter()

# set path and log file name
base_dir = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(base_dir, "templates")))


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def submit_job(item: SubmitJob):
    return create_job(item)


@router.get("/logtest")
async def get(request: Request):
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
    try:
        while True:
            await asyncio.sleep(1)
            logs = "test"
            await websocket.send_text(logs)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()
