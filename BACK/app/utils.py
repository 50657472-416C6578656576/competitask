from passlib.context import CryptContext
import os
import time
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_SECONDS = 1800  # 30 minutes
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "A OIPSc89A YySv8ds 8dv98w0uV(*)Y He v9sE)V_)( US)V*(WS0v9WSU)"
JWT_REFRESH_SECRET_KEY = "A OIPSc89A YySv8ds 8dv98w0uV(*)Y He v9sE)V_)( US)V*(WS0v9WSU)"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: str, expires_delta: int = None) -> str:
    delta = expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_SECONDS

    to_encode = {"exp": time.time() + delta, "subject": subject}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> str | None:
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return decoded['user_id'] if time.time() < decoded['exp'] else None
