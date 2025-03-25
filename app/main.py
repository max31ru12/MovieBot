import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config import TOKEN
from app.database.db_config import session_factory
from app.database.models import User
from app.routers.admin_router import router as admin_router


dp = Dispatcher()


dp.include_router(admin_router)


bot = Bot(token=TOKEN)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with session_factory() as session:
        user = User(
            tg_user_id=message.from_user.id, tg_username=message.from_user.username
        )
        session.add(user)
        await session.commit()
    await message.answer(
        "Для получения названия фильма подпишитесь на канал 1 и канал 2"
    )


@dp.message(Command("chat_info"))
async def show_chat_info(message: Message, bot: Bot):
    chat = message.chat
    await message.answer(f"ID чата: {chat.id}\nНазвание: {chat.title} {message.from_user.id}")


if __name__ == "__main__":
    asyncio.run(main())
