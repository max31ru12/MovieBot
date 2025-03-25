import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.config import TOKEN
from app.routers.admin_router import router as admin_router


dp = Dispatcher()


dp.include_router(admin_router)


bot = Bot(token=TOKEN)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Для получения названия фильма подпишитесь на канал 1 и канал 2")







@dp.message()
async def show_chat_info(message: Message, bot: Bot):
    chat = message.chat
    await message.answer(f"ID чата: {chat.id}\nНазвание: {chat.title}")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo,␣
    ˓→sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
        # But not all the types is supporte


if __name__ == "__main__":
    asyncio.run(main())
