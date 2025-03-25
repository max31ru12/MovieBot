from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.database.db_config import session_factory
from app.database.models import Movie
from app.utils import check_user_is_admin, check_user_is_creator

router = Router()


# Определяем класс состояний для сценария добавления фильма
class AddMovieState(StatesGroup):
    waiting_for_code = State()
    waiting_for_name = State()


@router.message(Command("add_movie"))
async def add_movie(message: Message, bot: Bot, state: FSMContext):
    is_admin = await check_user_is_admin(bot, message.from_user.id, message.chat.id)
    is_creator = await check_user_is_creator(bot, message.from_user.id, message.chat.id)

    if is_admin or is_creator or message.from_user.username == "maxevg72":
        await message.answer("Введите код фильма (целое число): ")
        await state.set_state(AddMovieState.waiting_for_code)
    else:
        await message.answer("Пошел нахуй отсюда")


@router.message(AddMovieState.waiting_for_code)
async def process_movie_code(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите числовой код фильма.")
        return

    code = int(message.text)

    await state.update_data(movie_code=code)
    await message.answer("Хорошо. Теперь введите название фильма:")
    await state.set_state(AddMovieState.waiting_for_name)


@router.message(AddMovieState.waiting_for_name)
async def process_movie_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name:
        await message.answer(
            "❗ Название фильма не может быть пустым. Введите название ещё раз:"
        )
        return

    data = await state.get_data()
    code = data.get("movie_code")

    async with session_factory() as session:
        movie = Movie(code=code, name=name)
        session.add(movie)
        await session.commit()

    await message.answer(f"✅ Фильм добавлен: <b>{code}</b> – {name}")

    await state.clear()
