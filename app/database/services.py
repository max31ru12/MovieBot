from sqlalchemy import select, desc

from app.database.db_config import session_factory
from app.database.models import User, Movie


class CodeAlreadyExistsError(Exception):
    pass


class NameAlreadyExistsError(Exception):
    pass


async def check_user_is_admin_db(username: str) -> bool:
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
            movie = (
                await session.execute(select(Movie).filter_by(code=code))
            ).scalar_one_or_none()
            if movie is not None:
                raise CodeAlreadyExistsError("Movie with provided code already exists")

        if name is not None:
            movie = (
                await session.execute(select(Movie).filter_by(name=name))
            ).scalar_one_or_none()
            if movie is not None:
                raise NameAlreadyExistsError("Movie with provided name already exists")


async def add_movie_to_db(code: int, message_id: int) -> None:
    async with session_factory() as session:
        movie = Movie(code=code, message_id=message_id)
        session.add(movie)
        await session.commit()


async def get_last_movie() -> Movie:
    async with session_factory() as session:
        result = await session.execute(select(Movie).order_by(desc(Movie.id)).limit(1))
        return result.scalar_one_or_none()


async def get_movie_by_code(code: int) -> Movie:
    async with session_factory() as session:
        result = await session.execute(select(Movie).filter_by(code=code))
        return result.scalar_one_or_none()


async def add_user_to_db(tg_user_id: int, tg_username: str) -> None:
    async with session_factory() as session:
        user = User(tg_user_id=tg_user_id, tg_username=tg_username, is_admin=False)
        session.add(user)
        await session.commit()
        return user


async def get_user_by_kwargs(**kwargs) -> User:
    async with session_factory() as session:
        result = await session.execute(select(User).filter_by(**kwargs))
        return result.scalar_one_or_none()
