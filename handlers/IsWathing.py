import sqlite3

from aiogram import BaseMiddleware
from aiogram.types import Update
import logging
from collections import defaultdict
import asyncio
from handlers.stb import throttling_time as tt, remove_time, remove_mes,standard_dep
#from handlers.database import add_user,player_exists
from handlers.database_ip import check_loot,add_user,player_exists
from handlers.database_ip import set_chat_rules,get_chat_rules

logging.basicConfig(level=logging.INFO)



class He(BaseMiddleware):
    def __init__(self):
        self.last_time = defaultdict(float)
        self.delay =  tt

    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            connect = sqlite3.connect("chats.db")
            cursor = connect.cursor()
            chat_id = event.message.chat.id
            chat_name = event.message.chat.title or "Личный чат"
            name = str()
            # Проверяем есть ли чат в БД
            rules = await get_chat_rules(chat_id)
            if rules == "Чат не найден":
                # Создаем с правилами по умолчанию
                default_rules = (chat_id, chat_name, 1, 1, 1, 1, 1, -500)
                await set_chat_rules(default_rules)
                logging.info(f"Созданы правила для нового чата: {chat_name}")
            try:
                cursor.execute("SELECT name FROM Chats WHERE id = ?", (event.message.chat.id,))
                name = cursor.fetchone()[0]
            except:
                logging.warning("Чат не найден")
                name = str(event.message.chat.id)
            finally:
                connect.close()

            logging.info(f"Запрос пришел, из чата: {name}")
            user_id = event.message.from_user.id
            current_time = asyncio.get_event_loop().time()
            is_exist = await player_exists(user_id)

            if not is_exist:
                await add_user(user_id, event.message.from_user.full_name)

            await check_loot(event.message, user_id, standard_dep)
            #Проверка на спам пользователя
            if current_time - self.last_time[user_id] < self.delay:
                logging.info(f"Спамер обнаружен: user_id ={user_id}// Chat_id = {event.message.chat.id}")

                text = event.message.text or ""
                if "крутка" in text.lower() or "лудка" in text.lower():
                    asyncio.create_task(remove_mes(message=event.message, time=remove_time -30))
                if text == "⛏️":
                    asyncio.create_task(remove_mes(message=event.message, time=remove_time - 30))
                return None  # пропускаем

            self.last_time[user_id] = current_time
        return await handler(event, data)

