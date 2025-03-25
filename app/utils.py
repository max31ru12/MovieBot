from aiogram import Bot
from aiogram.enums import ChatMemberStatus


async def check_subscription(bot: Bot, user_id: int, channel: int | str) -> bool:
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in {
            ChatMemberStatus.MEMBER,
        }
    except Exception as e:
        # Канал не найден, бот не имеет доступа, пользователь заблокировал бота и т.д.
        print(f"Ошибка при проверке подписки: {e}")
        return False


async def check_user_is_admin(bot: Bot, user_id: int, channel: int | str) -> bool:
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in {ChatMemberStatus.ADMINISTRATOR}
    except Exception as e:
        print(f"Ошибка при проверке пользователя в качестве администратора: {e}")
        return False


async def check_user_is_creator(bot: Bot, user_id: int, channel: int | str) -> bool:
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in {ChatMemberStatus.CREATOR}
    except Exception as e:
        print(f"Ошибка при проверке пользователя в качестве создателя: {e}")
        return False


async def check_all_roles(bot: Bot, user_id: int, channel: int | str) -> bool:
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in {
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
        }
    except Exception as e:
        print(f"Ошибка при проверке пользователя в качестве создателя: {e}")
        return False
