from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.database.services import (
    add_movie_to_db,
    CodeAlreadyExistsError,
    NameAlreadyExistsError,
    check_movie_exists,
    get_last_movie,
)
from app.keyboards.admin_keyboard import base_admin_menu, cancel_movie_admin_menu
from app.utils import check_user_is_admin, check_user_is_creator

router = Router()


# Определяем класс состояний для сценария добавления фильма
class AddMovieState(StatesGroup):
    waiting_for_code = State()
    waiting_for_name = State()


@router.message(F.text == "📥 Добавить фильм")
async def add_movie(message: Message, bot: Bot, state: FSMContext):
    is_admin = await check_user_is_admin(bot, message, message.chat.id)
    is_creator = await check_user_is_creator(bot, message.from_user.id, message.chat.id)

    if is_admin or is_creator:
        await message.answer(
            "Введите код фильма (целое число): ",
            reply_markup=cancel_movie_admin_menu,
        )
        await state.set_state(AddMovieState.waiting_for_code)
    else:
        await message.answer("Пошел нахуй отсюда")


@router.message(AddMovieState.waiting_for_code)
async def process_movie_code(message: Message, state: FSMContext):
    if message.text == "Отменить добавление фильма":
        await state.clear()
        await message.answer(
            "🚫 Добавление фильма отменено.", reply_markup=base_admin_menu
        )
        return

    if not message.text.isdigit():
        await message.answer(
            "❗ Пожалуйста, введите числовой код фильма.",
            reply_markup=cancel_movie_admin_menu,
        )
        return

    code = int(message.text)

    try:
        await check_movie_exists(code=code)
        await state.update_data(movie_code=code)
        await message.answer(
            "Хорошо. Теперь введите название фильма:",
            reply_markup=cancel_movie_admin_menu,
        )
        await state.set_state(AddMovieState.waiting_for_name)
        return
    except CodeAlreadyExistsError:
        await message.answer(
            "Фильм с таким кодом уже существует", reply_markup=cancel_movie_admin_menu
        )


@router.message(AddMovieState.waiting_for_name)
async def process_movie_name(message: Message, state: FSMContext):
    # Отмена добавления фильма
    if message.text == "Отменить добавление фильма":
        await state.clear()
        await message.answer(
            "🚫 Добавление фильма отменено.", reply_markup=base_admin_menu
        )
        return

    name = message.text.strip()

    if not name:
        await message.answer(
            "❗ Название фильма не может быть пустым. Введите название ещё раз:",
            reply_markup=cancel_movie_admin_menu,
        )
        return

    data = await state.get_data()
    code = data.get("movie_code")

    try:
        await check_movie_exists(name=name)
        await add_movie_to_db(code, name)
        await message.answer(f"✅ Фильм добавлен: <b>{code}</b> – {name}")
        await state.clear()
    except NameAlreadyExistsError:
        await message.answer(
            "Фильм с таким именем уже существует", reply_markup=base_admin_menu
        )
        return


@router.message(F.text == "Отменить добавление фильма")
async def process_cancel_adding_movie(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Добавление фильма отменено.", reply_markup=base_admin_menu)


@router.message(F.text == "Последний фильм")
async def get_last_movie_info(message: Message):
    last_movie = await get_last_movie()
    await message.answer(
        f"<b>Код:</b> {last_movie.code} \n<b>Название:</b> {last_movie.name}",
        parse_mode="HTML",
    )
