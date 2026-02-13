import logging

from aiogram import F, types
from aiogram import Router
from asyncio import sleep, create_task
from aiogram.types import ReactionTypeEmoji
router = Router()
from handlers.stb import Dice_time as dt,casino,is_win,remove_time, remove_mes


@router.message((F.text.lower().split().contains("крутка")) | (F.text.lower().split().contains("лудка")))
async def fortuna_case_insensitive_handler(message: types.Message):
    stack_of_loot = []
    keyword = None
    mes = None  # объявляем заранее

    try:
        match = message.text.lower().split(' ')

        if "крутка" in match:
            keyword = "крутка"
        elif "лудка" in match:
            keyword = "лудка"
        else:
            return

        indexnum = match.index(keyword)

        try:
            num = int(match[indexnum + 1])
        except (IndexError, ValueError):
            num = 5

        if num > 10:
            num = 10
            if keyword == "лудка":
                mes = await message.reply("Многовато чёт, десятки хватит")
        elif num < 0:
            num = 3
            if keyword == "лудка":
                mes = await message.reply("Я воспринимаю только отрицательный баланс")
        else:
            if keyword == "лудка":
                mes = await message.reply("Крутим, крутим!")

        for _ in range(num):
            if keyword == "крутка":
                ludka = await message.answer_dice(emoji=casino)
            else:
                ludka = await message.reply_dice(emoji=casino)

            stack_of_loot.append(ludka)
            await sleep(dt)

        if keyword == "лудка" and mes:
            await mes.delete()

    except Exception as e:
        print(e)
    finally:
        for i in stack_of_loot:
            if i and i.dice.value not in (1, 22, 43, 64):
                try:
                    create_task(remove_mes(i, dt))
                except:
                    pass
            else:
                emo = await is_win(i)
                if emo is not None:
                    await i.react([ReactionTypeEmoji(emoji=emo)])
                    create_task(remove_mes(i, remove_time))
        try:
            create_task(remove_mes(message, remove_time))
            print("Запрос обработан!")
        except Exception as e:
            logging.info(f"Не получилось удалить сообщение: {e}")
            pass



