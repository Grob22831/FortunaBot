from aiogram import Bot, Dispatcher,Router
import asyncio
from handlers.__init__ import connect_dis
from handlers.stb import token
#from aiogram.fsm.storage.redis import RedisStorage
#from redis.asyncio import Redis
#redis = Redis(host='localhost')
#storage = RedisStorage(redis)

router = Router()


tbot = Bot(token = token)
async def main()->None:

    dp = Dispatcher()
    # создал роутер, добавь его в диспетчер
    connect_dis(dp)
    await dp.start_polling(tbot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is dead")



