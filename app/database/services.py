from sqlalchemy import select

from app.database.db_config import session_factory
from app.database.models import User, Movie


class CodeAlreadyExistsError(Exception):
    pass


class NameAlreadyExistsError(Exception):
    pass


async def check_user_is_admin_db(username: str):
    async with session_factory() as session:
        stmt = select(User).filter_by(tg_username=username)
        result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        return False
    return user.is_admin


async def check_movie_exists(code: int | None = None, name: str | None = None):
    async with session_factory() as session:
        if code is not None:
            movie = (await session.execute(select(Movie).filter_by(code=code))).scalar_one_or_none()
            if movie is not None:
                raise CodeAlreadyExistsError("Movie with provided code already exists")

        if name is not None:
            movie = (await session.execute(select(Movie).filter_by(name=name))).scalar_one_or_none()
            if movie is not None:
                raise NameAlreadyExistsError("Movie with provided name already exists")


async def add_movie_to_db(code: int, name: str):
    async with session_factory() as session:
        movie = Movie(code=code, name=name)
        session.add(movie)
        await session.commit()
