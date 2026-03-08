import logging
from aiogram import types
import emoji
from asyncio import sleep
from handlers._queue import  queue_manager

throttling_time = 2
Dice_time = 2
remove_time = 60
standard_dep =50
casino_chat =1003727753341


#emojy
casino = emoji.emojize(":slot_machine:")
trophy = emoji.emojize(":trophy:")
cool = emoji.emojize("😎")
tada = emoji.emojize("🎉")
imp = emoji.emojize("👏")
omg = emoji.emojize("😱")
pickaxe = emoji.emojize("⛏️")

Coefficients = {"777":28, "lll":16, "ggg":9, "bbb":5}

async def is_win(message: types.Message):
    if message.dice and message.dice.emoji == casino:
        if int(message.dice.value) == 64:
            return trophy
        elif int(message.dice.value) == 1:
            return imp
        elif int(message.dice.value) == 22:
            return tada
        elif int(message.dice.value) == 43:
            return cool
    return None

#удаление сообщения
async def remove_mes(message: types.Message, time: int):
    await sleep(time)
    try:
        await message.delete()
    except Exception as e:
        logging.warning(f"Не удалось удалить сообщение: {e}")












