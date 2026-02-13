from aiogram.filters import Command
from aiogram import types,Router,Bot
from handlers.stb import  casino_chat

router = Router()
#позволяет писать от имени бота в чате в котором присутствует бот
@router.message(Command("talk"))
async def bot_talk(message: types.Message,bot:Bot):
    message_text = message.text.split(" ")

    if len(message_text) < 3:
        await message.reply("У меня не получилось обработать запрос (")
        return

    chat_id = message_text[1]
    if chat_id == "casino":
        chat_id = casino_chat
    text = " ".join(message_text[2:])

    await bot.send_message(chat_id=chat_id, text=text)
    await message.reply("У меня получилось обработать запрос )")


