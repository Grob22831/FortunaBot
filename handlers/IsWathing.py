from aiogram import BaseMiddleware
from aiogram.types import Update,Message
import logging
from collections import defaultdict
import asyncio
from handlers.stb import trottling_time as tt, remove_time, remove_mes,check_loot,standart_dep
from handlers.database import add_user,player_exists

logging.basicConfig(level=logging.INFO)

class He(BaseMiddleware):
    def __init__(self):
        self.last_time = defaultdict(float)
        self.delay =  tt

    async def __call__(self, handler, event: Update, data: dict):
        logging.info(f"Запрос пришел, из чата: {event.message.chat.id}")

        if event.message:
            user_id = event.message.from_user.id
            current_time = asyncio.get_event_loop().time()
            is_exist = await player_exists(user_id)
            if not is_exist:
                await add_user(user_id, event.message.from_user.full_name)
            await check_loot(event.message,user_id,standart_dep)
            if current_time - self.last_time[user_id] < self.delay:
                logging.info(f"Спамер обнаружен: user_id ={user_id}// Chat_id = {event.message.chat.id}")

                text = event.message.text or ""
                if "крутка" in text.lower() or "лудка" in text.lower():
                    asyncio.create_task(remove_mes(message=event.message, time=remove_time -30))
                return None  # пропускаем

            self.last_time[user_id] = current_time
        return await handler(event, data)

