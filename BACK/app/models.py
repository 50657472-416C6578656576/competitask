from sqlalchemy import String, create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, nickname={self.nickname!r}, email={self.email!r})"


url = 'sqlite:///competask.db'
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
