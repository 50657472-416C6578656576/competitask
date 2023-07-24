from sqlalchemy import create_engine, select, MetaData, or_
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
import uuid

from app.schemas import SignupSchemaRequest, UserSchemaResponse
from app.utils import verify_password, get_hashed_password
from app.models import User

import sqlite3


url = 'sqlite:///competask.db'
if not database_exists(url):
    create_database(url)
engine = create_engine(url, echo=True)


def add_user(user: SignupSchemaRequest):
    with Session(engine) as session:
        user_id = str(uuid.uuid4())
        new_user = User(user_id=user_id, nickname=user.nickname,
                        email=user.email, password=get_hashed_password(user.password))
        session.add(new_user)
        session.commit()
        return user_id


def select_user(nickname: str | None, email: str | None):
    with Session(engine) as session:
        if nickname and email:
            stmt = select(User).where(or_(User.nickname == nickname, User.email == email))
        elif nickname:
            stmt = select(User).where(User.nickname == nickname)
        elif email:
            stmt = select(User).where(User.email == email)
        else:
            return
        return session.execute(stmt).first()


def select_all_users():
    with Session(engine) as session:
        res = []
        stmt = select(User)
        for row in session.execute(stmt):
            user = row[0]
            res.append(UserSchemaResponse(nickname=user.nickname, email=user.email,
                                          password=user.password, user_id=user.user_id))
        return res
