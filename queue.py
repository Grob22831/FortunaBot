#Очередь
import asyncio
import logging
from collections import defaultdict, deque


class RequestQueue:
    def __init__(self):
        self.queues = defaultdict(deque)  # очередь для каждого чата
        self.processing = defaultdict(bool)  # флаг обработки

    async def add(self, chat_id, coro):
        """Добавить задачу в очередь"""
        self.queues[chat_id].append(coro)
        if not self.processing[chat_id]:
            asyncio.create_task(self.process_queue(chat_id))

    async def process_queue(self, chat_id):
        """Обработать очередь для конкретного чата"""
        self.processing[chat_id] = True
        while self.queues[chat_id]:
            coro = self.queues[chat_id].popleft()
            try:
                await coro
            except Exception as e:
                logging.error(f"Ошибка в очереди: {e}")
            await asyncio.sleep(1)  # задержка 1 сек между запросами в один чат
        self.processing[chat_id] = False


queue_manager = RequestQueue()