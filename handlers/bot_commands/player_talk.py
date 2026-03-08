from asyncio import create_task, sleep
from os import getenv
import logging
from dotenv import load_dotenv
from aiogram import types, Router, Bot, F
from aiogram.filters import Command

from handlers.stb import remove_mes, casino_chat
from handlers.database_ip import set_chat_rules, get_chat_rules_str, get_chat_rules_dict, get_users_list, get_stats, check_loot
from handlers._queue import queue_manager

load_dotenv()
router = Router()


##################### ID чата #########################
@router.message(Command("chat"))
async def bot_get_chat(message: types.Message):
    chat_id = str(message.chat.id)
    chat_name = str(message.chat.full_name)
    await message.answer(chat_id=int(getenv("general_headquarters")),
                         text=f"Вот тебе маленький дедосер -{chat_name} - {chat_id} id этого чата")
    create_task(remove_mes(message, 3))


@router.message(Command("get_chat_id"))
async def get_chat_id(message: types.Message):
    rules = await get_chat_rules_dict(message.chat.id)
    if rules['m_chat_commands'] == 0:
        mes = await message.reply("Тут такое нельзя")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return
    chat_id = str(message.chat.id)
    await message.reply(f"Я знаю что тебе надо: {chat_id}")


##################### Правила чата ####################
@router.message(Command("set_rules"))
async def set_chat_rules_cmd(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    if user_status.status not in ["administrator", "creator"] and not message.from_user.id == int(getenv("general_headquarters")):
        mes = await message.reply("❌ Только администраторы могут изменять правила")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    mes = message.text.split(" ")
    if len(mes) < 7:
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
        rules = (chat_id, chat_name, m_slots, m_chat_commands, m_reactions, m_welcome, m_work, min_balance)

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
    rules_text = await get_chat_rules_str(chat_id)

    if rules_text == "Чат не найден":
        default_rules = (chat_id, chat_name, 1, 1, 1, 1, 1, -500)
        await set_chat_rules(default_rules)
        rules_text = (f"Название: {chat_name}\nСлоты: on\nКоманды: on\nРеакции: on\n"
                      f"Приветствия: on\nРабота: on\nМин.баланс: -500")
        mes = await message.reply(f"✅ Правила не найдены — созданы новые\n\n{rules_text}")
    else:
        mes = await message.reply(f"📋 Текущие правила:\n{rules_text}")

    create_task(remove_mes(message, 15))
    create_task(remove_mes(mes, 30))


################# Разговор бота ######################
@router.message(Command("talk"))
async def bot_talk(message: types.Message, bot: Bot):
    parts = message.text.split(" ")
    if len(parts) < 3:
        await message.reply("У меня не получилось обработать запрос (")
        return
    chat_id = parts[1]
    if chat_id == "casino":
        chat_id = casino_chat
    text = " ".join(parts[2:])
    await bot.send_message(chat_id=chat_id, text=text)
    await message.reply("✅ Ответ отправлен")


################# Команды игроков ######################
@router.message(Command('get_users'))
async def get_users(message: types.Message):
    user_status = await message.chat.get_member(message.from_user.id)
    if (user_status.status not in ["administrator", "creator"]
            and not message.from_user.id == int(getenv("general_headquarters"))):
        mes = await message.answer("❌ Только администраторы могут получать данные о всех пользователях")
        create_task(remove_mes(message, 10))
        create_task(remove_mes(mes, 10))
        return

    async def process_execute(msg: types.Message):
        try:
            list_of_users = "Вот все лудики🥰:\n" + await get_users_list()
            sent_msg = await msg.answer(list_of_users)
            logging.info(f"Сообщение отправлено в чат {msg.chat.id}, message_id={sent_msg.message_id}")
            create_task(remove_mes(msg, 25))
            create_task(remove_mes(sent_msg, 25))
        except Exception as e:
            logging.error(f"Ошибка при отправке /get_users: {e}")

    queue_id = message.chat.id
    await queue_manager.add(queue_id, process_execute, message)


@router.message(Command('get_stats'))
async def get_my_stats(message: types.Message):
    async def process_execute(msg: types.Message):
        try:
            user_id = msg.from_user.id
            stats_text = "Ты есть у меня в списке🌚:\n" + await get_stats(user_id)
            sent_msg = await msg.answer(stats_text)
            logging.info(f"Сообщение отправлено в чат {msg.chat.id}, message_id={sent_msg.message_id}")
            create_task(remove_mes(msg, 25))
            create_task(remove_mes(sent_msg, 25))
        except Exception as e:
            logging.error(f"Ошибка при отправке /get_stats: {e}")

    queue_id = message.chat.id
    await queue_manager.add(queue_id, process_execute, message)