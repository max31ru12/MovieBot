from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from app.config import bot, CHANNEL_ONE_ID, MOVIE_CHANNEL_ID
from app.keyboards.user_keyboard import (
    channels_to_subscribe_user_menu,
    base_user_menu,
    already_subscribed_user_menu,
    cancel_movie_user_menu,
)
from app.messages import UserMessages
from app.utils.check_permissions import check_subscription
from app.utils.utils import forward_movie_message

router = Router()


class GetMovieName(StatesGroup):
    waiting_for_code = State()


@router.message(F.text == UserMessages.GET_MOVIE_BY_CODE.value)
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
    if message.text == UserMessages.CANCEL_GETTING_MOVIE.value:
        await state.clear()
        await message.answer("Ввод фильма отменен", reply_markup=base_user_menu)
        return

    await forward_movie_message(bot, message, cancel_movie_user_menu)
    # TODO какая-нибудь рекламная хуйня
    await message.answer("Узнать еще название", reply_markup=base_user_menu)


@router.callback_query(F.data == UserMessages.CHECK_SUBSCRIPTION.value)
async def process_already_subscribed(callback: CallbackQuery):
    user_id = callback.from_user.id

    access = await check_subscription(
        bot, user_id, CHANNEL_ONE_ID
    ) and await check_subscription(bot, user_id, MOVIE_CHANNEL_ID)

    if access:
        await callback.message.edit_reply_markup(
            reply_markup=already_subscribed_user_menu
        )
        await callback.message.answer("✅ Подтверждено!", reply_markup=base_user_menu)
    else:
        await callback.message.answer(
            "Для получения доступа подпишитесь на следующие каналы",
            reply_markup=channels_to_subscribe_user_menu,
        )


@router.message(F.text == UserMessages.CANCEL_GETTING_MOVIE.value)
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
