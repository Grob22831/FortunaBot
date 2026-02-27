import logging
from handlers.database_ip import check_loot
from aiogram import F, types, Router
from aiogram.types import ReactionTypeEmoji
from asyncio import sleep, create_task
from handlers.stb import pickaxe, remove_time, remove_mes, standard_dep
import sqlite3,random
from handlers.database_ip import get_balance,change_balance
router = Router()
from queue import queue_manager


@router.message(F.text == pickaxe)
async def work_on_job(message: types.Message):
    async def proces_execute():  # оборачиваем логику в функцию
        salary = random.randint(0, 30)

        if salary == 0:
            text = "Тебе не удалось накопать ничего ценного🪨. Зарплата: 0"
        elif salary < 6:
            text = f"Даже уголь чего-то стоит🔥. Зарплата: {salary}"
        elif salary < 16:
            text = f"Тебе удалось найти железо⛓️. Зарплата: {salary}"
        else:
            text = f"Тебе удалось найти алмазы💎. Зарплата: {salary}"

        mess = await message.reply(text, disable_notification=True)
        balance = await get_balance(message.from_user.id)
        await change_balance(message.from_user.id, salary + balance)

        try:
            await remove_mes(message, remove_time - 20)
            await remove_mes(mess, remove_time - 30)
        except:
            logging.error("Не удалось удалить сообщение")

    # Добавляем задачу в очередь
    await queue_manager.add(message.chat.id, proces_execute())


