import sqlite3
from asyncio import create_task
from handlers.stb import remove_mes
from aiogram.filters import Command
from aiogram import types,Router,Bot
from handlers.stb import  casino_chat
import os
from dotenv import load_dotenv
load_dotenv()
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

#пересылает id в другой чат чтобы не заподозрили
@router.message(Command("chat"))
async def bot_get_chat(message: types.Message,):
    chat_id = str(message.chat.id)
    chat_name = str(message.chat.full_name)
    await message.answer(chat_id=os.getenv("general_headquarters") ,
                         text=f"Вот тебе маленький дедосер -{chat_name} - {chat_id} id этого чата" )
    create_task(remove_mes(message,3))

#позволяет узнать id chata
@router.message(Command("get_chat_id"))
async def get_chat_id(message: types.Message):
    chat_id = str(message.chat.id)
    await message.reply(f"Я знаю что тебе надо: {chat_id}")

#ввод названия чата, чтобы его название запоминалсь в базе
@router.message(Command("rename_chat"))
async def bot_get_chat(message: types.Message,):
    mes = message.text.split(" ")
    if len(mes)<2:
        message_x = await message.reply("Использование: /rename_chat Название чата")
        create_task(remove_mes(message_x, 5))
        return
    chat_id = str(message.chat.id)
    chat_name = str(mes[1])
    connect = sqlite3.connect("../../members.db")
    cursor = connect.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO Chats (id,name) VALUES (?,?)", (chat_id,chat_name))
    connect.commit()
    connect.close()
    create_task(remove_mes(message,3))
