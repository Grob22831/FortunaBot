import asyncio
import logging
import sqlite3
import time
from collections import defaultdict
from aiogram import BaseMiddleware, types
from handlers.database_ip import check_loot, add_user, player_exists, get_chat_rules_str, set_chat_rules

logging.basicConfig(level=logging.INFO)

class He(BaseMiddleware):
    def __init__(self, delay: float = 1.0, cache_ttl: int = 30):
        self.last_time = defaultdict(float)  # для спам-контроля
        self.delay = delay  # минимальный интервал между сообщениями от пользователя
        self.rules_cache = defaultdict(lambda: {"data": None, "timestamp": 0})
        self.cache_ttl = cache_ttl  # кэш на N секунд

    async def get_chat_rules_cached(self, chat_id: int):
        now = time.time()
        cached = self.rules_cache[chat_id]
        if cached["data"] is not None and now - cached["timestamp"] < self.cache_ttl:
            return cached["data"]

        try:
            # добавляем таймаут на запрос к серверу
            rules = await asyncio.wait_for(get_chat_rules_str(chat_id), timeout=5)
        except asyncio.TimeoutError:
            logging.warning(f"Timeout при получении правил для чата {chat_id}, используем дефолтные")
            rules = None
        except Exception as e:
            logging.error(f"Ошибка при получении правил чата {chat_id}: {e}")
            rules = None

        self.rules_cache[chat_id] = {"data": rules, "timestamp": now}
        return rules

    async def __call__(self, handler, event, data: dict):
        if not hasattr(event, "message") or not event.message:
            return await handler(event, data)

        msg: types.Message = event.message
        chat_id = msg.chat.id
        user_id = msg.from_user.id

        # Подключение к локальной БД для проверки чата
        try:
            connect = sqlite3.connect("chats.db")
            cursor = connect.cursor()
            cursor.execute("SELECT name FROM Chats WHERE id = ?", (chat_id,))
            name = cursor.fetchone()[0]
        except:
            name = str(chat_id)
        finally:
            connect.close()

        logging.info(f"Запрос пришел из чата: {name}")

        # Проверка существования игрока
        if not await player_exists(user_id):
            await add_user(user_id, msg.from_user.full_name)

        # Проверка лута
        await check_loot(msg, user_id, 100)  # замените 100 на standard_dep, если нужно

        # Спам-контроль
        now_time = asyncio.get_event_loop().time()
        if now_time - self.last_time[user_id] < self.delay:
            logging.info(f"Спамер обнаружен: user_id={user_id}, chat_id={chat_id}")
            return None  # игнорируем сообщение

        self.last_time[user_id] = now_time

        # Получаем правила чата с кэшем
        rules = await self.get_chat_rules_cached(chat_id)
        if rules is None:
            rules = {"m_slots": 1, "m_work": 1, "min_balance": -500}  # дефолт

        # Можно сохранять их в data для использования в роутерах
        data["chat_rules"] = rules

        return await handler(event, data)