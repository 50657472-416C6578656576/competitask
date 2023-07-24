from enum import StrEnum, auto
from uuid import UUID
from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class SignupSchemaRequest(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class LoginSchemaRequest(BaseModel):
    email: EmailStr
    password: str


class AvailableSignupDataSchemeResponse(BaseModel):
    available: bool
    taken_email: bool = False
    taken_nickname: bool = False
    message: str | None = None
