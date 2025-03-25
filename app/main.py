import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config import TOKEN
from app.keyboards.admin_keyboard import admin_start_keyboard
from app.routers.admin_router import router as admin_router


dp = Dispatcher()


dp.include_router(admin_router)


bot = Bot(token=TOKEN)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Для получения названия фильма подпишитесь на канал 1 и канал 3",
        reply_markup=admin_start_keyboard,
    )


@dp.message(Command("chat_info"))
async def show_chat_info(message: Message, bot: Bot):
    chat = message.chat
    await message.answer(
        f"ID чата: {chat.id}\nНазвание: {chat.title} {message.from_user.id}"
    )


if __name__ == "__main__":
    asyncio.run(main())
