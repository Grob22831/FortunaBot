from  aiogram import Dispatcher

from handlers.bot_commands.start import router as start_
from handlers.bot_commands.talk import router as talk_router
from handlers.bot_commands.players import router as players_router
#from handlers.inline import router as inline_
from handlers.on_chat_message.Fortune import router as fortune_
from handlers.on_chat_message.reaction import router as reaction_
from handlers.IsWathing import He


def connect_dis(dp: Dispatcher):
    dp.update.middleware(He())

    #команды
    dp.include_router(talk_router)
    dp.include_router(start_)
    dp.include_router(players_router)
    #сообщения
    dp.include_router(fortune_)


    dp.include_router(reaction_)





