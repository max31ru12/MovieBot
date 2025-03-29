from aiogram import Bot
from aiogram.types import Message

from app.config import MOVIE_CHANNEL_ID
from app.database.services import get_movie_by_code


async def forward_movie_message(bot: Bot, message: Message, cancel_keyboard):
    if not message.text.isdigit():
        await message.answer(
            "❗ Пожалуйста, введите числовой код фильма.",
            reply_markup=cancel_keyboard,
        )
        return

    code = int(message.text)
    movie = await get_movie_by_code(code)

    if movie is None:
        await message.answer(
            "❗ Фильма с указанным кодом нет", reply_markup=cancel_keyboard
        )
    else:
        await bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=MOVIE_CHANNEL_ID,
            message_id=movie.message_id,
        )
