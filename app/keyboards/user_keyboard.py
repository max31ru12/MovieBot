from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.config import CHANNEL_ONE_NAME, MOVIE_CHANNEL_NAME

base_user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Узнать название фильма")],
        [KeyboardButton(text="Подписаться на каналы")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
    one_time_keyboard=False,
)


already_subscribed_user_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Я подписался")]], resize_keyboard=True
)


channels_to_subscribe_user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Подписаться на {CHANNEL_ONE_NAME}",
                url="https://t.me/movietestkanal1",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Подписаться на канал {MOVIE_CHANNEL_NAME}",
                url="https://t.me/movietestkanal2",
            )
        ],
    ]
)


cancel_movie_user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить ввод фильма")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


full_user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить ввод фильма")],
        [KeyboardButton(text="Узнать название фильма")],
        [KeyboardButton(text="Подписаться на каналы")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
