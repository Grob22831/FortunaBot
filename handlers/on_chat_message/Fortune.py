import logging
from handlers.database_ip import check_loot, get_balance,get_chat_rules_dict
from aiogram import F, types, Router
from aiogram.types import ReactionTypeEmoji
from asyncio import sleep, create_task
from handlers.stb import Dice_time as dt, casino, is_win, remove_time, remove_mes, standard_dep,pickaxe
import sqlite3
router = Router()

from _queue import queue_manager

@router.message(F.text)
async def fortuna_case_insensitive_handler(message: types.Message):

    text = message.text.lower()
    if "крутка" not in text and "лудка" not in text:
        return

    rules = await get_chat_rules_dict(message.chat.id)
    if rules is not None and rules['m_slots'] == 0:
        mes = await message.reply("❌ Слоты отключены в этом чате")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    async def proces_execute():
        stack_of_loot = []
        keyword = None
        mes_ = None

        rules_ = await get_chat_rules_dict(message.chat.id)
        min_balance = -500 if rules_ is None else rules_['min_balance']

        if await get_balance(message.from_user.id) <= min_balance:
            mesige = await message.reply(
                "Ты и так в долгах. Чертов капитализм!?"
                f"\n Отправь {pickaxe} чтобы сходить на работу"
            )
            await remove_mes(mesige, remove_time - 30)
            await remove_mes(message, remove_time - 30)
            return

        try:
            match = message.text.lower().split()

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
                    mes_ = await message.reply("Многовато чёт, десятки хватит")
            elif num < 0:
                num = 3
                if keyword == "лудка":
                    mes_ = await message.reply("Я воспринимаю только отрицательный баланс")
            else:
                if keyword == "лудка":
                    mes_ = await message.reply("Крутим, крутим!")

            for _ in range(num):
                if keyword == "крутка":
                    ludka = await message.answer_dice(emoji=casino)
                else:
                    ludka = await message.reply_dice(emoji=casino, disable_notification=True)

                await check_loot(ludka, message.from_user.id, standard_dep)
                stack_of_loot.append(ludka)
                await sleep(dt)

            if keyword == "лудка" and mes_:
                await mes_.delete()

        except Exception as e:
            print(e)

        finally:
            for i in stack_of_loot:
                if i and i.dice.value not in (1, 22, 43, 64):
                    create_task(remove_mes(i, dt))
                else:
                    emo = await is_win(i)
                    if emo:
                        await i.react([ReactionTypeEmoji(emoji=emo)])
                        create_task(remove_mes(i, remove_time))

            try:
                create_task(remove_mes(message, remove_time))
                connect = sqlite3.connect("../../members.db")
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT username FROM Players WHERE user_id = ?",
                    (message.from_user.id,)
                )
                row = cursor.fetchone()
                username = row[0] if row else "unknown"
                connect.close()

                logging.info(f"Запрос обработан! для пользователя:{username}")
            except:
                pass

    queue_id = (message.chat.id, message.message_thread_id or 0)
    await queue_manager.add(queue_id, proces_execute)
