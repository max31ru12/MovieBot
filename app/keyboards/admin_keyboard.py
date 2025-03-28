from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📥 Добавить фильм"),
            KeyboardButton(text="Последний фильм"),
            KeyboardButton(text="Фильм по коду"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


cancel_adding_movie_admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отменить добавление фильма")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)

cancel_getting_movie_admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отменить получение фильма")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
