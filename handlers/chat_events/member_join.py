from asyncio import create_task
from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER
from handlers.stb import remove_mes
from _queue import queue_manager
from handlers.database_ip import get_chat_rules_dict


router = Router()


#сообщение встречающее пользователя который входит в чат
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def chat_member_join(event: types.ChatMemberUpdated):
    rules = await get_chat_rules_dict(event.chat.id)
    if rules['m_welcome'] == 0:
        return
    async def process_execute():
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
    await queue_manager.add(event.chat.id,process_execute,event, getattr(event, 'message_thread_id', None) )


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def chat_member_leave(event: types.ChatMemberUpdated):
    async  def process_execute():
        user = event.old_chat_member.user
        chat = event.chat

        message = await event.bot.send_message(
            chat_id=chat.id,
            text=f"Ну и не надо, ну и пожалуйста, {user.first_name} 👋"
        )
        create_task(remove_mes(message, 100))
    queue_manager.add(event.chat.id,process_execute,event, getattr(event, 'message_thread_id', None))