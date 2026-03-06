import asyncio
import logging
from collections import defaultdict, deque


class RequestQueue:
    def __init__(self):
        self.queues = defaultdict(deque)
        self.processing = defaultdict(bool)

    async def add(self, queue_id, coro_func, *args, **kwargs):
        self.queues[queue_id].append((coro_func, args, kwargs))

        if not self.processing[queue_id]:
            self.processing[queue_id] = True
            asyncio.create_task(self.process_queue(queue_id))

    async def process_queue(self, queue_id):
        while True:
            if not self.queues[queue_id]:
                self.processing[queue_id] = False
                return

            coro_func, args, kwargs = self.queues[queue_id].popleft()

            try:
                await coro_func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Ошибка в очереди: {e}")

            await asyncio.sleep(1)


queue_manager = RequestQueue()