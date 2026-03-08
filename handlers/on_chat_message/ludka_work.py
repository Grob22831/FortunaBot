import logging
import random
from asyncio import sleep, create_task
from handlers.database_ip import (
    check_loot, get_balance, get_chat_rules_dict, change_balance
)
from aiogram import F, types, Router
from aiogram.types import ReactionTypeEmoji
from handlers.stb import (
    Dice_time as dt, casino, is_win, remove_time, remove_mes, standard_dep, pickaxe
)
from handlers._queue import queue_manager

router = Router()

# -----------------------------
# Обработка команд "крутка" и "лудка"
# -----------------------------
@router.message(F.text.lower().contains("крутка") | F.text.lower().contains("лудка"))
async def fortuna_case_insensitive_handler(message: types.Message):
    rules = await get_chat_rules_dict(message.chat.id)
    if rules is not None and rules['m_slots'] == 0:
        mes = await message.reply("❌ Слоты отключены в этом чате")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    async def process_execute(msg: types.Message, thread_id: int):
        stack_of_loot = []
        keyword = None
        mes_ = None

        rules_ = await get_chat_rules_dict(msg.chat.id)
        min_balance = -500 if rules_ is None else rules_['min_balance']

        if await get_balance(msg.from_user.id) <= min_balance:
            mesige = await msg.reply(
                "Ты и так в долгах. Чертов капитализм!?"
                f"\n Отправь {pickaxe} чтобы сходить на работу"
            )
            await remove_mes(mesige, remove_time - 30)
            await remove_mes(msg, remove_time - 30)
            return

        try:
            match = msg.text.lower().split()

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
                    mes_ = await msg.reply("Многовато чёт, десятки хватит", message_thread_id=thread_id)
            elif num < 0:
                num = 3
                if keyword == "лудка":
                    mes_ = await msg.reply("Я воспринимаю только отрицательный баланс", message_thread_id=thread_id)
            else:
                if keyword == "лудка":
                    mes_ = await msg.reply("Крутим, крутим!")

            for _ in range(num):
                if keyword == "крутка":
                    ludka = await msg.answer_dice(emoji=casino)
                else:
                    ludka = await msg.reply_dice(emoji=casino, disable_notification=True)

                await check_loot(ludka, msg.from_user.id, standard_dep)
                stack_of_loot.append(ludka)
                await sleep(dt)

            if keyword == "лудка" and mes_:
                await mes_.delete()

        except Exception as e:
            logging.exception(e)

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
                logging.info(f"Запрос обработан! {getattr(msg.from_user, 'username', 'Unknown')}")
            except:
                pass

    queue_id = (message.chat.id, message.message_thread_id or 0)
    await queue_manager.add(queue_id, process_execute, message, message.message_thread_id)

# -----------------------------
# Работа с "⛏️"
# -----------------------------
@router.message(F.text == pickaxe)
async def work_on_job(message: types.Message):
    rules = await get_chat_rules_dict(message.chat.id)
    if rules is not None and rules['m_work'] == 0:
        mes = await message.reply("В этом чате запрещено работать!")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    async def proces_execute():
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

    await queue_manager.add(message.chat.id, proces_execute)