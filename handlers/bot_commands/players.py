from asyncio import create_task

from flask.cli import load_dotenv

from handlers.database_ip import get_users_list,clear_users_list, get_stats
from aiogram.filters import Command
from aiogram import types,Router
from handlers.stb import remove_mes
from queue import queue_manager
router = Router()
from dotenv import load_dotenv
from os import getenv
load_dotenv()
#выводит список игроков, их имя, баланс
@router.message(Command('get_users'))
async def get_users(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    if user_status.status not in ["administrator", "creator"] and not message.from_user.id == getenv(
            "general_headquarters"):
        mes = await message.reply("❌ Только администраторы могут получать данные о всех пользователях")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return
    async def process_execute():
        list_of_users = "Вот все лудики🥰:\n" + await get_users_list()
        stats = await message.answer(list_of_users)
        create_task(remove_mes(message, 25))
        create_task(remove_mes(stats, 25))
    queue_manager.add(message.chat.id,process_execute())
#выводит информацию о тебе
@router.message(Command('get_stats'))
async def get_users(message: types.Message):
    async def process_execute():
        user_id = message.from_user.id
        stats = "Ты есть у меня в списке🌚:\n" + await get_stats(user_id)
        stats = await message.answer(stats)
        create_task(remove_mes(message, 25))
        create_task(remove_mes(stats, 25))
    queue_manager.add(message.chat.id, process_execute())

#удаляет из списка всех игроков
#@router.message(Command('clear_users'))
#async def clear_users(message: types.Message):
#
#    async def process_execute():
#        await clear_users_list()
#        stats = await message.answer("Список очищен, сладенький🤭")
#        create_task(remove_mes(message, 25))
#        create_task(remove_mes(stats, 25))
#    queue_manager.add(message.chat.id, process_execute())