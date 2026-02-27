import logging
from handlers.database_ip import check_loot, get_balance
from aiogram import F, types, Router
from aiogram.types import ReactionTypeEmoji
from asyncio import sleep, create_task
from handlers.stb import Dice_time as dt, casino, is_win, remove_time, remove_mes, standard_dep,pickaxe
import sqlite3
router = Router()
from queue import queue_manager

@router.message((F.text.lower().split().contains("крутка")) | (F.text.lower().split().contains("лудка")))
async def fortuna_case_insensitive_handler(message: types.Message):

    async def proces_execute():
        stack_of_loot = []
        keyword = None
        mes = None

        if await get_balance(message.from_user.id) <= -1 * standard_dep * 10:
            mesige = await message.reply("Ты и так в долгах. Чертов капитализм!?"
                                         f"\n Отправь {pickaxe} чтобы сходить на работу")
            await remove_mes(mesige, remove_time - 30)
            await remove_mes(message, remove_time - 30)
            return

        try:
            match = message.text.lower().split(' ')

            if "крутка" in match:
                keyword = "крутка"
            elif "лудка" in match:
                keyword = "лудка"
            else:
                return

            index_num = match.index(keyword)

            try:
                num = int(match[index_num + 1])
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
                    ludka = await message.reply_dice(emoji=casino, disable_notification=True)
                await check_loot(ludka, message.from_user.id, standard_dep)

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
                connect = sqlite3.connect("../../members.db")
                cursor = connect.cursor()
                cursor.execute(f"SELECT username FROM Players WHERE user_id = {message.from_user.id}")
                username = cursor.fetchone()[0]
                connect.close()
                logging.info(f"Запрос обработан! для пользователя:{username} ")
            except:
                pass
        await queue_manager.add(message.chat.id,proces_execute())
