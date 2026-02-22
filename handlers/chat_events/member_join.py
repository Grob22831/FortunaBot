from asyncio import create_task
from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER
from handlers.stb import remove_mes
router = Router()

#сообщение встречающее пользователя который входит в чат
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def chat_member_join(event: types.ChatMemberUpdated):
        user_id = event.new_chat_member.user.id
        user_name = event.new_chat_member.user.username
        chat = event.chat
        message =await event.bot.send_message(
            chat_id=chat.id,
            text=f"Привет, {user_name}! Добро пожаловать в чат.\n"
                 f"Что ты можешь делать:\n"
                 f"Крутить - крути сам, или напиши крутка - тогда я буду высылать крутки за тебя.\n"
                 f"За каждую крутку с баланса списываются баллы, за победу начисляются.\n"
                 f"Хочешь узнать о себе в этом чате - пиши /get_stats.\n"
        )
        create_task(remove_mes(message, 100))


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def chat_member_leave(event: types.ChatMemberUpdated):
    user = event.old_chat_member.user
    chat = event.chat

    message = await event.bot.send_message(
        chat_id=chat.id,
        text=f"Ну и не надо, ну и пожалуйста, {user.first_name} 👋"
    )
    create_task(remove_mes(message, 100))