from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.database.services import add_movie_to_db, CodeAlreadyExistsError, NameAlreadyExistsError, check_movie_exists
from app.keyboards.admin_keyboard import adding_film_adding_keyboard
from app.utils import check_user_is_admin, check_user_is_creator

router = Router()


# Определяем класс состояний для сценария добавления фильма
class AddMovieState(StatesGroup):
    waiting_for_code = State()
    waiting_for_name = State()


@router.message(F.text == "📥 Добавить фильм")
async def add_movie(message: Message, bot: Bot, state: FSMContext):
    is_admin = (await check_user_is_admin(bot, message, message.chat.id))
    is_creator = await check_user_is_creator(bot, message.from_user.id, message.chat.id)

    if is_admin or is_creator:
        await message.answer("Введите код фильма (целое число): ", reply_markup=adding_film_adding_keyboard)
        await state.set_state(AddMovieState.waiting_for_code)
    else:
        await message.answer("Пошел нахуй отсюда")


@router.message(AddMovieState.waiting_for_code)
async def process_movie_code(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите числовой код фильма.")
        return

    code = int(message.text)

    try:
        await check_movie_exists(code=code)
        await state.update_data(movie_code=code)
        await message.answer("Хорошо. Теперь введите название фильма:", reply_markup=adding_film_adding_keyboard)
        await state.set_state(AddMovieState.waiting_for_name)
        return
    except CodeAlreadyExistsError:
        await message.answer("Фильм с таким кодом уже существует")


@router.message(AddMovieState.waiting_for_name)
async def process_movie_name(message: Message, state: FSMContext):

    # Отмена добавления фильма
    if message.text == "Отменить ввод фильма":
        await state.clear()
        await message.answer("🚫 Добавление фильма отменено.")
        return

    name = message.text.strip()

    if not name:
        await message.answer(
            "❗ Название фильма не может быть пустым. Введите название ещё раз:"
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
        await message.answer("Фильм с таким именем уже существует")
        return


@router.message(F.text == "Отменить ввод фильма")
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять. Вы не находитесь в процессе добавления.")
        return

    await state.clear()
    await message.answer("🚫 Добавление фильма отменено.")

