from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📥 Добавить фильм"),
            KeyboardButton(text="Последний фильм"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)

cancel_film_adding_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отменить ввод фильма")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
