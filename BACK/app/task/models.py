from sqlalchemy import String, Integer, DateTime, create_engine, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship

from app.engine import engine
from app.task.schemas import TaskSchemaResponse


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"
    task_id = mapped_column(String, primary_key=True)
    parent_id = mapped_column(String, ForeignKey("task.task_id"))
    user_id = mapped_column(String)
    title = mapped_column(String(100), nullable=False)
    description = mapped_column(String)
    subtasks_num = mapped_column(Integer, nullable=False, default=0)
    completed_num = mapped_column(Integer, nullable=False, default=0)
    completed = mapped_column(Boolean)
    active = mapped_column(Boolean)

    def schema(self):
        return TaskSchemaResponse(
            task_id=self.task_id,
            parent_id=self.parent_id,
            user_id=self.user_id,
            title=self.title,
            description=self.description,
            subtasks_num=self.subtasks_num,
            completed_num=self.completed_num,
            completed=self.completed,
            active=self.active,
            subtasks=[],
        )

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, task_id={self.task_id!r}, parent_id={self.parent_id!r})"


Base.metadata.create_all(engine)
