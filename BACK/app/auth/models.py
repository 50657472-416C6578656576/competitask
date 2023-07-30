from sqlalchemy import String, Integer, DateTime, create_engine, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship

from app.auth.schemas import UserSchemaResponse
from app.engine import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    user_id = mapped_column(String, primary_key=True)
    username = mapped_column(String(30), unique=True, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String)

    def schema(self):
        return UserSchemaResponse(user_id=self.user_id, email=self.email, username=self.username)

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, email={self.email!r}, id={self.user_id!r})"


Base.metadata.create_all(engine)
