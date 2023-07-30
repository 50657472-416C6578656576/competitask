from enum import StrEnum, auto
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from datetime import date


class Message(BaseModel):
    message: str


class DayOfTheWeek(StrEnum):
    monday = auto()
    tuesday = auto()
    wednesday = auto()
    thursday = auto()
    friday = auto()
    saturday = auto()
    sunday = auto()


class TaskSchemaRequest(BaseModel):
    parent_id: str | None = None
    title: str
    description: str | None = None
    planned_date: date | None = None
    refresh_days: list[DayOfTheWeek] | None = None
    subtasks: list['TaskSchemaRequest'] | None = None


class TaskSchemaResponse(BaseModel):
    user_id: str
    task_id: str
    parent_id: str | None = None
    title: str
    description: str | None = None
    planned_date: date | None = None
    refresh_days: list[DayOfTheWeek] | None = None
    subtasks_num: int
    completed_num: int
    completed: bool
    active: bool
    subtasks: list['TaskSchemaResponse'] | None = None
