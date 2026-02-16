from asyncio import create_task

from handlers.database_ip import get_users_list,clear_users_list, get_stats
from aiogram.filters import Command
from aiogram import types,Router
from handlers.stb import remove_mes

router = Router()

#выводит список игроков, их имя, баланс
@router.message(Command('get_users'))
async def get_users(message: types.Message):
    list_of_users ="Вот все лудики🥰:\n" + await get_users_list()
    stats = await message.answer(list_of_users)
    create_task(remove_mes(message, 25))
    create_task(remove_mes(stats, 25))
#выводит информацию о тебе
@router.message(Command('get_stats'))
async def get_users(message: types.Message):
    user_id = message.from_user.id
    stats ="Ты есть у меня в списке🌚:\n" + await get_stats(user_id)
    stats=await message.answer(stats)
    create_task(remove_mes(message,25))
    create_task(remove_mes(stats,25))

#удаляет из списка всех игроков
@router.message(Command('clear_users'))
async def clear_users(message: types.Message):
    await clear_users_list()
    stats =await message.answer("Список очищен, сладенький🤭")
    create_task(remove_mes(message, 25))
    create_task(remove_mes(stats, 25))