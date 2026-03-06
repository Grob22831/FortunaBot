import asyncio
import logging
from collections import defaultdict, deque


class RequestQueue:
    def __init__(self):
        self.queues = defaultdict(deque)
        self.processing = defaultdict(bool)

    async def add(self, chat_id, coro):
        self.queues[chat_id].append(coro)

        if not self.processing[chat_id]:
            self.processing[chat_id] = True
            asyncio.create_task(self.process_queue(chat_id))

    async def process_queue(self, chat_id):
        while True:
            if not self.queues[chat_id]:
                self.processing[chat_id] = False
                return

            coro = self.queues[chat_id].popleft()

            try:
                await coro
            except Exception as e:
                logging.error(f"Ошибка в очереди: {e}")

            await asyncio.sleep(1)


queue_manager = RequestQueue()