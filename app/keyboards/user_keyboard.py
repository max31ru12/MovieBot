from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.config import CHANNEL_ONE_NAME, CHANNEL_TWO_NAME

user_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Узнать название фильма")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


channels_to_subscribe_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Подписаться на {CHANNEL_ONE_NAME}",
                url="https://t.me/movietestkanal1",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Подписаться на канал {CHANNEL_TWO_NAME}",
                url="https://t.me/movietestkanal2",
            )
        ],
    ]
)
