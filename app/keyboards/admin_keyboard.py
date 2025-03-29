from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.messages import AdminMessages

base_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить фильм"),
            KeyboardButton(text="Получить фильм по коду"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


cancel_getting_movie_admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=AdminMessages.CANCEL_GETTING_MOVIE.value)]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


cancel_adding_movie_admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=AdminMessages.CANCEL_ADDING_MOVIE.value)]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
