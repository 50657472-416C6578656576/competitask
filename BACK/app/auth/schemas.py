from enum import StrEnum, auto
from uuid import UUID
from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class SignupSchemaRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginSchemaRequest(BaseModel):
    email: EmailStr
    password: str


class ValidationResult(BaseModel):
    valid: bool
    message: str | None = None


class AvailableSignupDataSchemaResponse(BaseModel):
    
    email: ValidationResult
    username: ValidationResult


class UserSchemaResponse(BaseModel):
    user_id: str
    username: str
    email: EmailStr
