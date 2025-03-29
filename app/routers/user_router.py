from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.config import bot, CHANNEL_ONE_ID, MOVIE_CHANNEL_ID
from app.database.services import get_movie_by_code
from app.keyboards.user_keyboard import (
    channels_to_subscribe_user_menu,
    base_user_menu,
    already_subscribed_user_menu,
    cancel_movie_user_menu,
)
from app.utils import check_subscription

router = Router()


class GetMovieName(StatesGroup):
    waiting_for_code = State()


@router.message(F.text == "Узнать название фильма")
async def get_movie_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    access = await check_subscription(
        bot, user_id, CHANNEL_ONE_ID
    ) and await check_subscription(bot, user_id, MOVIE_CHANNEL_ID)

    if access:
        await message.answer("Введите код фильма", reply_markup=cancel_movie_user_menu)
        await state.set_state(GetMovieName.waiting_for_code)
    else:
        await message.answer(
            "Для получения доступа подпишитесь на следующие каналы",
            reply_markup=channels_to_subscribe_user_menu,
        )
        return


@router.message(GetMovieName.waiting_for_code)
async def process_user_input_code(message: Message, state: FSMContext):
    if message.text == "Отменить ввод фильма":
        await state.clear()
        await message.answer("Ввод фильма отменен", reply_markup=base_user_menu)
        return

    if not message.text.isdigit():
        await message.answer(
            "❗ Пожалуйста, введите числовой код фильма.",
            reply_markup=cancel_movie_user_menu,
        )
        return

    code = int(message.text)
    movie = await get_movie_by_code(code)

    if movie is None:
        await message.answer(
            "❗ Фильма с указанным кодом нет", reply_markup=cancel_movie_user_menu
        )
    else:
        await bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=MOVIE_CHANNEL_ID,
            message_id=movie.message_id,
        )


@router.message(F.text == "Подписаться на каналы")
async def show_subscribe_info(message: Message):
    await message.answer(
        "Для получения доступа подпишитесь на следующие каналы",
        reply_markup=channels_to_subscribe_user_menu,
    )

    await message.answer("Уже подписаны?", reply_markup=already_subscribed_user_menu)


@router.message(F.text == "Я подписался")
async def process_already_subscribed(message: Message):
    await message.answer("Отлично!", reply_markup=base_user_menu)


@router.message(F.text == "Отменить ввод фильма")
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нечего отменять. Вы не находитесь в процессе добавления.",
            reply_markup=base_user_menu,
        )
        return

    await state.clear()
    await message.answer("🚫 Получение фильма отменено.", reply_markup=base_user_menu)
