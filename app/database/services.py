from sqlalchemy import select

from app.database.db_config import session_factory
from app.database.models import User, Movie


async def check_user_is_admin_db(username: str):
    async with session_factory() as session:
        stmt = select(User).filter_by(tg_username=username)
        result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        return False
    return user.is_admin


async def add_movie(code: int, name: str):
    async with session_factory() as session:
        movie = Movie(code=code, name=name)
        session.add(movie)
        await session.commit()
