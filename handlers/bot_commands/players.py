from asyncio import create_task
from handlers.database_ip import get_users_list, get_stats
from aiogram.filters import Command
from aiogram import types, Router
from handlers.stb import remove_mes
from handlers._queue import queue_manager
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()
router = Router()


# -----------------------------
# Команда /get_users — список всех игроков
# -----------------------------
@router.message(Command('get_users'))
async def get_users(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    if (user_status.status not in ["administrator", "creator"]
            and not message.from_user.id == int(getenv("general_headquarters"))):
        mes = await message.answer("❌ Только администраторы могут получать данные о всех пользователях")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    async def process_execute(msg: types.Message):
        try:
            list_of_users = "Вот все лудики🥰:\n" + await get_users_list()
            sent_msg = await msg.answer(list_of_users)
            logging.info(f"Сообщение отправлено в чат {msg.chat.id}, message_id={sent_msg.message_id}")
            create_task(remove_mes(msg, 25))
            create_task(remove_mes(sent_msg, 25))
        except Exception as e:
            logging.error(f"Ошибка при отправке /get_users: {e}")

    queue_id = message.chat.id
    await queue_manager.add(queue_id, process_execute, message)


# -----------------------------
# Команда /get_stats — информация о себе
# -----------------------------
@router.message(Command('get_stats'))
async def get_my_stats(message: types.Message):
    async def process_execute(msg: types.Message):
        try:
            user_id = msg.from_user.id
            stats_text = "Ты есть у меня в списке🌚:\n" + await get_stats(user_id)
            sent_msg = await msg.answer(stats_text)
            logging.info(f"Сообщение отправлено в чат {msg.chat.id}, message_id={sent_msg.message_id}")
            create_task(remove_mes(msg, 25))
            create_task(remove_mes(sent_msg, 25))
        except Exception as e:
            logging.error(f"Ошибка при отправке /get_stats: {e}")

    queue_id = message.chat.id
    await queue_manager.add(queue_id, process_execute, message)