from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message

from app.config import MOVIE_CHANNEL_ID
from app.database.services import get_all_users, get_movie_by_id


async def forward_movie_message(bot: Bot, message: Message, cancel_keyboard):
    if not message.text.isdigit():
        await message.answer(
            "❗ Пожалуйста, введите числовой код фильма.",
            reply_markup=cancel_keyboard,
        )
        return

    code = int(message.text)
    movie = await get_movie_by_id(code)

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


async def broadcast(bot: Bot, text: str) -> None:
    users = await get_all_users()

    failed = 0

    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_user_id, text=text, parse_mode="HTML"
            )
        except TelegramForbiddenError:
            # пользователь заблокировал бота
            failed += 1
        except TelegramBadRequest as e:
            print(f"Ошибка отправки: {e}")
            failed += 1
