from collections import defaultdict

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
import uuid

from app.engine import engine
from app.task.models import Task
from app.task.schemas import TaskSchemaRequest


def task_exists(task_id: str | None):
    with Session(engine) as session:
        stmt = select(Task).where(Task.task_id == f"{task_id}")
        return (not task_id) or bool(session.execute(stmt).first())


def insert_task(user_id: str, task: TaskSchemaRequest, parent_id: str | None = None):
    with Session(engine) as session:
        if (not parent_id) and task_exists(task.parent_id):
            parent_id = task.parent_id
        sub_num = 0
        task_id = str(uuid.uuid4())

        if task.subtasks:
            for subtask in task.subtasks:
                sub_num += insert_task(user_id=user_id, task=subtask, parent_id=task_id)
        else:
            sub_num = 1

        new_task = Task(
            task_id=task_id,
            user_id=user_id,
            parent_id=parent_id,
            title=task.title,
            description=task.description,
            completed_num=0,
            completed=False,
            active=True,
            subtasks_num=sub_num,
        )
        session.add(new_task)
        session.commit()
        return sub_num


async def select_tasks(user_id: str):
    with Session(engine) as session:
        stmt = select(Task).where(Task.user_id == f"{user_id}")
        tasks = defaultdict(list)
        for task in session.execute(stmt):
            tasks[task[0].parent_id].append(task[0].schema())
        return tasks
