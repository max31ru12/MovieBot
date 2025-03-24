from sqlalchemy.orm import Mapped, mapped_column

from app.database.db_config import Base


class Movie(Base):

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
