import sqlite3
from asyncio import create_task

from PyInstaller.compat import getenv

from handlers.stb import remove_mes
from aiogram.filters import Command
from aiogram import types,Router,Bot, F
from handlers.stb import  casino_chat
import os
from handlers.database_ip import set_chat_rules,get_chat_rules
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
    rules = await get_chat_rules(message.chat.id)
    if rules['m_chat_commands'] == 0:
        mes = await message.reply("Тут такое нельзя")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return
    chat_id = str(message.chat.id)
    await message.reply(f"Я знаю что тебе надо: {chat_id}")


#####################Правила чата ######################
@router.message(Command("set_rules"))
async def set_chat_rules_cmd(message: types.Message):
    # Проверяем, является ли пользователь администратором чата
    user_status = await message.chat.get_member(message.from_user.id)
    if user_status.status not in ["administrator", "creator"] and not message.from_user.id == getenv("general_headquarters"):
        mes = await message.reply("❌ Только администраторы могут изменять правила")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    mes = message.text.split(" ")

    if len(mes) < 8:
        message_x = await message.reply(
            "Использование: /set_rules [слоты] [команды] [реакции] [приветствия] [работа] [мин_баланс]\n"
            "Пример: /set_rules on on on on on -500"
        )
        create_task(remove_mes(message_x, 10))
        return

    try:
        status_map = {"on": 1, "off": 0}

        m_slots = status_map[mes[1].lower()]
        m_chat_commands = status_map[mes[2].lower()]
        m_reactions = status_map[mes[3].lower()]
        m_welcome = status_map[mes[4].lower()]
        m_work = status_map[mes[5].lower()]
        min_balance = int(mes[6])

        chat_id = message.chat.id
        chat_name = message.chat.title or "Личный чат"

        rules = (chat_id, chat_name, m_slots, m_chat_commands,
                 m_reactions, m_welcome, m_work, min_balance)

        await set_chat_rules(rules)
        mes = await message.reply("✅ Правила чата обновлены")


    except KeyError:
        mes = await message.reply("❌ Ошибка: используйте 'on' или 'off'")
    except ValueError:
        mes = await message.reply("❌ Ошибка: баланс должен быть числом")
    except Exception as e:
        mes = await message.reply(f"❌ Ошибка: {e}")
    finally:
        create_task(remove_mes(mes, 10))

    create_task(remove_mes(message, 3))


@router.message(Command("get_rules"))
async def get_chat_rules_cmd(message: types.Message):
    chat_id = message.chat.id
    chat_name = message.chat.title or "Личный чат"

    rules_text = await get_chat_rules(chat_id)

    if rules_text == "Чат не найден":
        # Создаем правила по умолчанию
        default_rules = (chat_id, chat_name, 1, 1, 1, 1, 1, -500)
        await set_chat_rules(default_rules)

        # Показываем созданные правила
        rules_text = (f"Название: {chat_name}\n"
                      f"Слоты: on\n"
                      f"Команды: on\n"
                      f"Реакции: on\n"
                      f"Приветствия: on\n"
                      f"Работа: on\n"
                      f"Мин.баланс: -500")

        await message.reply(f"✅ Правила не найдены — созданы новые\n\n{rules_text}")
    else:
        await message.reply(f"📋 Текущие правила:\n{rules_text}")

    create_task(remove_mes(message, 30))

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
