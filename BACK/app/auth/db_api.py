from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
import uuid

from app.auth.schemas import SignupSchemaRequest, UserSchemaResponse
from app.auth.security_utils import get_hashed_password
from app.auth.models import User
from app.engine import engine


async def add_user(user: SignupSchemaRequest):
    with Session(engine) as session:
        user_id = str(uuid.uuid4())
        new_user = User(
            user_id=user_id,
            username=user.username,
            email=user.email,
            password=get_hashed_password(user.password),
        )
        session.add(new_user)
        session.commit()
        return user_id


async def select_user(username: str | None = None, email: str | None = None, user_id: str | None = None):
    with Session(engine) as session:
        if username and email:
            stmt = select(User).where(or_(User.username == username, User.email == email))
        elif username:
            stmt = select(User).where(User.username == username)
        elif email:
            stmt = select(User).where(User.email == email)
        elif user_id:
            stmt = select(User).where(User.user_id == user_id)
        else:
            return
        return session.execute(stmt).all()


async def select_all_users():
    with Session(engine) as session:
        res = []
        stmt = select(User)
        for row in session.execute(stmt):
            user = row[0]
            res.append(UserSchemaResponse(username=user.username, email=user.email, user_id=user.user_id))
        return res
