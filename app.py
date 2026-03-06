from aiogram import Bot, Dispatcher,Router
import asyncio,os
from dotenv import load_dotenv
from handlers.__init__ import connect_dis
from handlers.conect_session import init_http,close_http
router = Router()

load_dotenv()
tbot = Bot(token = os.getenv("token"))
async def main()->None:

    dp = Dispatcher()
    # создал роутер, добавь его в диспетчер
    connect_dis(dp)
    await dp.start_polling(tbot)

if __name__ == '__main__':
    try:
        init_http()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is dead")
        close_http()



