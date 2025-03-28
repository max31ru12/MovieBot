from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📥 Добавить фильм"),
            KeyboardButton(text="Последний фильм"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


cancel_movie_admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отменить добавление фильма")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
