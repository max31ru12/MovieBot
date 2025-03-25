from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db_config import session_factory
from app.utils import check_user_is_admin, check_user_is_creator

router = Router()


@router.message(Command("add_movie"))
async def add_movie(message: Message, bot: Bot):
    is_admin = await check_user_is_admin(bot, message.from_user.id, message.chat.id)
    is_creator = await check_user_is_creator(bot, message.from_user.id, message.chat.id)
    if is_admin or is_creator:
        async with session_factory() as session:
            pass
