from aiogram import Router, F
from aiogram.types import Message

from app.database.services import add_movie_to_db

router = Router()


def parse_post_text(message: Message) -> dict:
    text_by_lines = message.text.split("\n")
    return {
        line[: line.find(":")].strip(): line[line.find(":") + 1 :].strip()
        for line in text_by_lines
    }


@router.channel_post(F.text)
async def handle_channel_post(message: Message):
    parsed_message_text = parse_post_text(message)

    code = parsed_message_text["Код"]
    message_id = message.message_id

    try:
        await add_movie_to_db(code, message_id)
    except Exception as e:  # noqa
        await message.answer(text="Код уже занят")

    await message.answer("Был опубликован пост")
