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
from app.utils.deepseek import chat
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
        await message.answer("Введите код фильма:", reply_markup=cancel_movie_user_menu)
        await state.set_state(GetMovieName.waiting_for_code)
    else:
        await message.answer(
            "Для получения доступа подпишитесь на следующие каналы:",
            reply_markup=channels_to_subscribe_user_menu,
        )
        return


@router.message(GetMovieName.waiting_for_code)
async def process_user_input_code(message: Message, state: FSMContext):
    if message.text == UserMessages.CANCEL_GETTING_MOVIE.value:
        await state.clear()
        await message.answer("Ввод фильма отменен.", reply_markup=base_user_menu)
        return

    await forward_movie_message(bot, message, cancel_movie_user_menu)
    await state.clear()
    # TODO какая-нибудь рекламная хуйня
    await message.answer("Узнать еще название?", reply_markup=base_user_menu)


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
        await callback.message.answer(
            "Выберите действие...", reply_markup=base_user_menu
        )
    else:
        await callback.message.answer(
            "Вы еще не подписаны. Для получения доступа подпишитесь на следующие каналы:",
            reply_markup=channels_to_subscribe_user_menu,
        )


@router.callback_query(F.data == UserMessages.ALREADY_SUBSCRIBED.value)
async def choose_action(callback: CallbackQuery):
    await callback.message.answer("Выберите действие...", reply_markup=base_user_menu)


@router.message(F.text == UserMessages.CANCEL_GETTING_MOVIE.value)
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нечего отменять. Вы не находитесь в процессе получения фильма.",
            reply_markup=base_user_menu,
        )
        return

    await state.clear()
    await message.answer("🚫 Получение фильма отменено.", reply_markup=base_user_menu)


class WaitForDescription(StatesGroup):
    wait_for_movie_description = State()


@router.message(F.text == UserMessages.GET_MOVIE_BY_GENRE.value)
async def get_movie_by_mood(message: Message, state: FSMContext):
    await message.answer(
        "Расскажи, какой бы вы хотели посмотреть фильм",
        reply_markup=cancel_movie_user_menu,
    )
    if message.text:
        await state.set_state(WaitForDescription.wait_for_movie_description)
        await state.update_data(user_request=message.text)
    else:
        await message.answer("Введите данные...", reply_markup=cancel_movie_user_menu)
        return


@router.message(WaitForDescription.wait_for_movie_description)
async def process_movie_by_mood_user_request(message: Message, state: FSMContext):
    state = await state.get_data()
    user_request = state["user_request"]
    prompt = f"""
    Забудь весь предыдущий контекст.

    Ты — рекомендательная система по фильмам.

    Если запрос пользователя НЕ относится к фильмам или жанрам кино, верни строго фразу: ЗАПРОС НЕ ПРИНЯТ.

    Запрос пользователя:
    {user_request}

    Твоя задача:
    1. Определи, о каком жанре кино идёт речь в запросе (например: боевик, драма, фантастика, ужасы и т.д.).
    2. Подбери 3–4 фильма **исключительно этого жанра** из списка топ-100 IMDb.
    3. Обязательно включи один фильм, выпущенный до 2000 года.
    4. Остальные фильмы — после 2000 года.
    5. Ответ строго на русском языке.
    6. Не добавляй вступления, размышлений, объяснений.
    7. Не включай фильмы других жанров, даже если они частично подходят. Только чёткое соответствие жанру.
    8. Проверь, что названия фильмов корректны и не содержат случайных слов или ошибок.
    9. Форматируй ответ строго так:

    1. <b>Название</b> (год) — краткое описание (до 50 слов). Рейтинг IMDb: X.XX
    2. <b>Название</b> (год) — краткое описание (до 50 слов). Рейтинг IMDb: X.XX
    3. <b>Название</b> (год) — краткое описание (до 50 слов). Рейтинг IMDb: X.XX

    Если можешь, добавь 4-й пункт в таком же формате.

    Пример:
    1. <b>Терминатор 2: Судный день</b> (1991) — робот-защитник спасает подростка от нового киборга. Рейтинг IMDb: 8.6
    """

    ai_answer = await chat(prompt)
    await message.answer(text=ai_answer, parse_mode="HTML", reply_markup=base_user_menu)
