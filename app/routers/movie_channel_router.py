from aiogram import Router
from aiogram.types import Message


router = Router()


def parse_post_text(message: Message) -> dict:
    text_by_lines = message.text.split("\n")
    return {
        line[: line.find(":")].strip(): line[line.find(":") + 1 :].strip()
        for line in text_by_lines
    }


# @router.channel_post(F.text)
# async def handle_channel_post(message: Message):
#     await message.answer("Был опубликован пост")
