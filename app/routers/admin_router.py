from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.config import bot, MOVIE_CHANNEL_ID
from app.database.services import (
    add_movie_to_db,
    get_user_by_kwargs,
    update_movie_by_id,
)
from app.keyboards.admin_keyboard import (
    base_admin_menu,
    cancel_getting_movie_admin_menu,
    cancel_adding_movie_admin_menu,
    cancel_broadcast_admin_menu,
)
from app.messages import AdminMessages
from app.utils.utils import forward_movie_message, broadcast

router = Router()


class AddFilmState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_genre = State()
    waiting_for_photo = State()


@router.message(F.text == AdminMessages.ADD_MOVIE.value)
async def start_adding_film(message: Message, state: FSMContext):
    user_db = await get_user_by_kwargs(tg_username=message.from_user.username)
    if user_db is None or not user_db.is_admin:
        await message.answer("Тебе сюда нельзя, убирайся!")
        return

    await state.set_state(AddFilmState.waiting_for_title)
    await message.answer(
        "Введите название фильма: ", reply_markup=cancel_adding_movie_admin_menu
    )


@router.message(AddFilmState.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddFilmState.waiting_for_description)
    await message.answer(
        "Введите описание фильма: ", reply_markup=cancel_adding_movie_admin_menu
    )


@router.message(AddFilmState.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddFilmState.waiting_for_genre)
    await message.answer(
        "Введите жанр/жанры фильма", reply_markup=cancel_adding_movie_admin_menu
    )


@router.message(AddFilmState.waiting_for_genre)
async def process_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text.strip())
    await state.set_state(AddFilmState.waiting_for_photo)
    await message.answer(
        "Пришлите фото (постер) фильма:", reply_markup=cancel_adding_movie_admin_menu
    )


@router.message(AddFilmState.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    # Здесь бы по-хорошему сделать транзакцию
    movie = await add_movie_to_db()

    data = await state.get_data()
    file_id = message.photo[-1].file_id
    post_text = (
        f"<b>Название:</b> {data['title']}\n"
        f"<b>Код:</b> {movie.id}\n"
        f"<b>Жанр:</b> {data['genre']}\n"
        f"<b>Описание:</b> {data['description']}"
    )

    post = await bot.send_photo(
        chat_id=MOVIE_CHANNEL_ID,
        photo=file_id,
        caption=post_text,
        parse_mode="HTML",
    )

    message_id = int(post.message_id)

    await update_movie_by_id(movie_id=movie.id, message_id=message_id)
    await message.answer("✅ Фильм опубликован в канале!", reply_markup=base_admin_menu)
    await state.clear()


class GetMovieByAdmin(StatesGroup):
    waiting_for_code = State()


@router.message(F.text == AdminMessages.GET_MOVIE_BY_CODE.value)
async def get_movie_by_code_admin(message: Message, state: FSMContext):
    user_db = await get_user_by_kwargs(tg_username=message.from_user.username)
    if user_db is None or not user_db.is_admin:
        await message.answer("Тебе сюда нельзя, убирайся!")
        return
    await message.answer(
        "Введите числовой код фильма", reply_markup=cancel_getting_movie_admin_menu
    )
    await state.set_state(GetMovieByAdmin.waiting_for_code)


@router.message(GetMovieByAdmin.waiting_for_code)
async def process_code_input_admin(message: Message, state: FSMContext):
    if message.text == AdminMessages.CANCEL_GETTING_MOVIE.value:
        await state.clear()
        await message.answer("Ввод фильма отменен", reply_markup=base_admin_menu)
        return

    await forward_movie_message(bot, message, cancel_getting_movie_admin_menu)
    await message.answer("Выберите действие...", reply_markup=base_admin_menu)


class BroadcastState(StatesGroup):
    waiting_for_message = State()


@router.message(F.text == AdminMessages.BROADCAST_MESSAGE.value)
async def start_broadcasting_message(message: Message, state: FSMContext):
    user_db = await get_user_by_kwargs(tg_username=message.from_user.username)
    if user_db is None or not user_db.is_admin:
        await message.answer("Тебе сюда нельзя, убирайся!")
        return

    await message.answer(
        "Введите сообщение: ", reply_markup=cancel_broadcast_admin_menu
    )
    await state.set_state(BroadcastState.waiting_for_message)


@router.message(BroadcastState.waiting_for_message)
async def broadcast_message(message: Message, state: FSMContext):
    if message.text == AdminMessages.CANCEL_BROADCAST.value:
        await state.clear()
        await message.answer("Рассылка отменена", reply_markup=base_admin_menu)
        return

    await broadcast(bot, message.text)
    await state.clear()
    await message.answer("Рассылка заверешена!", reply_markup=base_admin_menu)


# всякие отменялки внизу


@router.message(F.text == AdminMessages.CANCEL_ADDING_MOVIE.value)
async def process_cancel_adding_movie(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нечего отменять. Вы не находитесь в процессе добавления.",
            reply_markup=base_admin_menu,
        )
        return
    await state.clear()
    await message.answer("🚫 Добавление фильма отменено.", reply_markup=base_admin_menu)


@router.message(F.text == AdminMessages.CANCEL_BROADCAST.value)
async def process_cancel_broadcast(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нечего отменять. Вы не находитесь в процессе рассылки.",
            reply_markup=base_admin_menu,
        )
        return
    await message.answer("Рассылка отменена", reply_markup=base_admin_menu)
    await state.clear()
