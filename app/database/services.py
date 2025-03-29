from sqlalchemy import select, update

from app.database.db_config import session_factory
from app.database.models import User, Movie


async def check_user_is_admin_db(username: str) -> bool:
    async with session_factory() as session:
        stmt = select(User).filter_by(tg_username=username)
        result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        return False
    return user.is_admin


async def add_movie_to_db(message_id: int | None = None) -> Movie:
    async with session_factory() as session:
        movie = Movie(message_id=message_id)
        session.add(movie)
        await session.commit()
        return movie


async def update_movie_by_id(movie_id: int, message_id: int) -> None:
    async with session_factory() as session:
        stmt = update(Movie).where(Movie.id == movie_id).values(message_id=message_id)
        await session.execute(stmt)
        await session.commit()


async def get_movie_by_id(movie_id: int) -> Movie:
    async with session_factory() as session:
        result = await session.execute(select(Movie).filter_by(id=movie_id))
        return result.scalar_one_or_none()


async def add_user_to_db(tg_user_id: int, tg_username: str) -> User:
    async with session_factory() as session:
        user = User(tg_user_id=tg_user_id, tg_username=tg_username, is_admin=False)
        session.add(user)
        await session.commit()
        return user


async def get_user_by_kwargs(**kwargs) -> User:
    async with session_factory() as session:
        result = await session.execute(select(User).filter_by(**kwargs))
        return result.scalar_one_or_none()
