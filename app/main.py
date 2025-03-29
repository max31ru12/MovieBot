import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config import bot
from app.database.services import get_user_by_kwargs, add_user_to_db
from app.keyboards.admin_keyboard import base_admin_menu
from app.keyboards.user_keyboard import channels_to_subscribe_user_menu
from app.routers.admin_router import router as admin_router
from app.routers.user_router import router as user_router
from app.routers.movie_channel_router import router as movie_channel_router

dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_router)
dp.include_router(movie_channel_router)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    username = message.from_user.username
    user_id = message.from_user.id
    user_db = await get_user_by_kwargs(tg_username=username)

    if user_db is None:
        await add_user_to_db(user_id, username)
        is_admin = False
    else:
        is_admin = user_db.is_admin

    if is_admin:
        await message.answer(
            "Добро пожаловать",
            reply_markup=base_admin_menu,
        )
    else:
        await message.answer(
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            "📢 Для использования бота нужно подписаться на каналы.\n"
            "После подписки нажмите кнопку ниже ⬇️",
            reply_markup=channels_to_subscribe_user_menu,
        )


@dp.message(Command("chat_info"))
async def show_chat_info(message: Message, bot: Bot):
    chat = message.chat
    await message.answer(
        f"ID чата: {chat.id}\nНазвание: {chat.title} {message.from_user.id}"
    )


if __name__ == "__main__":
    asyncio.run(main())
