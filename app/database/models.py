from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db_config import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    tg_username: Mapped[str] = mapped_column(unique=True)
