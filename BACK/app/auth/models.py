from sqlalchemy import String, Integer, DateTime, create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    user_id = mapped_column(String, primary_key=True)
    nickname = mapped_column(String(30), unique=True)
    email = mapped_column(String, unique=True)
    password = mapped_column(String)

    def __repr__(self) -> str:
        return f"User(nickname={self.nickname!r}, email={self.email!r}, id={self.user_id!r})"


class Task(Base):
    __tablename__ = "task"
    task_id = mapped_column(String, primary_key=True)
    parent_id = mapped_column(String)
    title = mapped_column(String(100))
    description = mapped_column(String)
    update = mapped_column(Integer)
    expire = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"User(title={self.title!r}, task_id={self.task_id!r}, parent_id={self.parent_id!r})"


url = 'sqlite:///competask.db'
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
