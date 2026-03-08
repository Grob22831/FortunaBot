import logging
from handlers.database_ip import get_chat_rules_dict
from aiogram import F, types, Router
from asyncio import create_task
from handlers.stb import pickaxe, remove_time, remove_mes
import random
from handlers.database_ip import get_balance,change_balance
router = Router()
from handlers._queue import queue_manager

@router.message(F.text == pickaxe)
async def work_on_job(message: types.Message):
    rules = await get_chat_rules_dict(message.chat.id)
    if  rules is not None and rules['m_work'] == 0:
        mes =await message.reply("В этом чате запрещено работать!")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return
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
    await queue_manager.add(message.chat.id, proces_execute)


