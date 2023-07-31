from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.auth.routers import proper_token
from app.auth.db_api import select_user
from app.task.db_api import insert_task, select_tasks
from app.task.schemas import TaskSchemaRequest, TaskSchemaResponse, Message
from app.task.utils import tree_from_list

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.post("/set_tasks", response_model=bool)
async def set_tasks(tasks: list[TaskSchemaRequest], request: Request):
    user_data = await proper_token(request)
    if not (user_data and (await select_user(user_id=user_data["user_id"]))):
        return JSONResponse(status_code=401, content=Message(message="Unauthorized").dict())

    for task in tasks:
        insert_task(task=task, user_id=user_data["user_id"])
    return True


@router.get("/get_tasks", response_model=list[TaskSchemaResponse])
async def get_tasks(request: Request):
    user_data = await proper_token(request)
    if not (user_data and (await select_user(user_id=user_data["user_id"]))):
        return JSONResponse(status_code=401, content=Message(message="Unauthorized").dict())

    tasks = await select_tasks(user_id=user_data["user_id"])
    return tree_from_list(tasks=tasks)
