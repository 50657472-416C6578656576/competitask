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


class SignupSchemaRequest(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class LoginSchemaRequest(BaseModel):
    email: EmailStr
    password: str


class UserSchemaResponse(BaseModel):
    user_id: str
    nickname: str
    email: EmailStr
    password: str


class AvailableSignupDataSchemeResponse(BaseModel):
    available: bool
    taken_email: bool = False
    taken_nickname: bool = False
    message: str | None = None


class MakeListRequest(BaseModel):
    title: str
    description: str | None = None


class AddTaskRequest(BaseModel):
    list_id: UUID
    title: str
    description: str | None = None
    planned_date: date | None = None
    refresh_days: list[DayOfTheWeek] | None = None


class Task(BaseModel):
    list_id: UUID
    title: str
    description: str | None = None
    planned_date: date | None = None
    refresh_days: list[DayOfTheWeek] | None = None
    subtasks: list['Task'] | None = None


class ListById(BaseModel):
    title: str
    description: str | None = None
    task_list: list[Task]
