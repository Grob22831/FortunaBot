import sqlite3
from asyncio import create_task
from handlers.stb import remove_mes
from aiogram.filters import Command
from aiogram import types,Router,Bot, F
from handlers.stb import  casino_chat
import os
from dotenv import load_dotenv
from asyncio import sleep
load_dotenv()
router = Router()




##################### ID чата #########################
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



##################### Запоминание чата ######################
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
    connect = sqlite3.connect("chats.db")
    cursor = connect.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO Chats (id,name) VALUES (?,?)", (chat_id,chat_name))
    connect.commit()
    connect.close()
    await sleep(0.1)
    create_task(remove_mes(message,3))


################# Разговор бота ######################

# позволяет писать от имени бота в чате в котором присутствует бот
@router.message(Command("talk"))
async def bot_talk(message: types.Message, bot: Bot):
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


@router.message(F.reply_to_message)
async def forward_to_private(message: types.Message,bot:Bot):
    if message.reply_to_message.from_user.id == bot.id:
        # Информация об оригинале
        original_chat_id = message.chat.id
        original_chat_name = message.chat.title or message.chat.first_name
        original_message_id = message.message_id
        original_user = message.from_user.full_name

        # Формируем подпись
        caption = (f"👤 От: {original_user}\n"
                   f"💬 Чат: {original_chat_name}\n"
                   f"🆔 Chat ID: {original_chat_id}\n"
                   f"📨 Msg ID: {original_message_id}")

        # Копируем в личку с подписью
        await message.bot.copy_message(
            chat_id=os.getenv("general_headquarters"),  # твой личный ID
            from_chat_id=original_chat_id,
            message_id=original_message_id,
            caption=caption
        )
    else:return


# Отправляем ответ в оригинальный чат
@router.message(F.chat.type == "private", F.reply_to_message)
async def reply_from_private(message: types.Message):
    replied = message.reply_to_message

    if not replied.caption:
        return

    import re
    chat_id_match = re.search(r"Chat ID: (-\d+|\d+)", replied.caption)
    msg_id_match = re.search(r"Msg ID: (\d+)", replied.caption)

    if chat_id_match and msg_id_match:
        target_chat_id = int(chat_id_match.group(1))
        target_msg_id = int(msg_id_match.group(1))


        await message.bot.send_message(
            chat_id=target_chat_id,
            text=f"📨 Ответ от {message.from_user.full_name}:\n\n{message.text}",
            reply_to_message_id=target_msg_id
        )

        # Подтверждение в личке
        await message.reply("✅ Ответ отправлен в чат")
