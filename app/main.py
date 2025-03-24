import asyncio

from aiogram import Bot, Dispatcher

from app.config import TOKEN


dp = Dispatcher()


async def main():
     bot = Bot(token=TOKEN)
     await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
