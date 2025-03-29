from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.config import CHANNEL_ONE_NAME, MOVIE_CHANNEL_NAME
from app.messages import UserMessages

base_user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserMessages.GET_MOVIE_BY_CODE.value)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
    one_time_keyboard=False,
)


already_subscribed_user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Подтверждено!",
                callback_data=UserMessages.CHECK_SUBSCRIPTION.value,
            )
        ]
    ],
    resize_keyboard=True,
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
        [
            InlineKeyboardButton(
                text="Уже подписаны?",
                callback_data=UserMessages.CHECK_SUBSCRIPTION.value,
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
