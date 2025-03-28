from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.config import bot, CHANNEL_ONE_ID, CHANNEL_TWO_ID
from app.database.services import get_movie_by_code
from app.keyboards.user_keyboard import channels_to_subscribe_menu
from app.utils import check_subscription

router = Router()


class GetMovieName(StatesGroup):
    waiting_for_code = State()


@router.message(F.text == "Узнать название фильма")
async def get_movie_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    access = await check_subscription(
        bot, user_id, CHANNEL_ONE_ID
    ) and await check_subscription(bot, user_id, CHANNEL_TWO_ID)

    if access:
        await message.answer("Введите код фильма")
        await state.set_state(GetMovieName.waiting_for_code)
    else:
        await message.answer(
            "Снала необходимо подписаться на канал",
            reply_markup=channels_to_subscribe_menu,
        )
        return


@router.message(GetMovieName.waiting_for_code)
async def process_user_input_code(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите числовой код фильма.")
        return

    code = int(message.text)

    movie = await get_movie_by_code(code)
    if movie is None:
        await message.answer("❗ Фильма с указанным кодом нет")
    else:
        await message.answer(f"<b>Название фильма:</b> {movie.name}", parse_mode="HTML")
