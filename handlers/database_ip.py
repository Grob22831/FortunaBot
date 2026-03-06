import os
from aiogram import types
from handlers.stb import casino, Coefficients
from dotenv import load_dotenv
from handlers.conect_session import get_session,syte_url





############SET members
async def add_user(user_id, username):
    data = {"user_id": user_id, "username": username, "balance":1000}
    session = await get_session()
    async with session.post(f"{syte_url}/add_user", json=data) as resp:
        return await resp.json()
    #request.post(f"{syte_url}/add_user", json=data)

async def change_spins(user_id,new_spins):
    data = {"user_id": user_id, "new_spins":new_spins}
    session = await get_session()
    async with session.post(f"{syte_url}/add_spins", json=data) as resp:
        return await resp.json()
    #request.post(f"{syte_url}/add_spins", json=data)

async def change_balance(user_id,new_balance):
    data = {"user_id": user_id, "new_balance":new_balance}
    session = await get_session()
    async with session.post(f"{syte_url}/add_balance", json=data) as resp:
        return await resp.json()
    #request.post(f"{syte_url}/add_balance", json=data)
#async def clear_users_list():
    #request.post(f"{syte_url}/clear_users_list")




#############  GET members
async def get_balance(user_id):
    #response = request.get(f"{syte_url}/get_balance/{user_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/get_balance/{user_id}") as resp:
        if resp.status == 200:
            data = await resp.json()
            return data.get("balance", 0)
    return 0

async def get_spins(user_id):
    #response = request.get(f"{syte_url}/get_spins/{user_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/get_spins/{user_id}") as resp:
        if resp.status == 200:
            data = await resp.json()
            return data.get("spins", 0)
    return 0

async def get_stats(user_id):
    #response = request.get(f"{syte_url}/get_stats/{user_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/get_stats/{user_id}") as resp:
        if resp.status == 200:
            data = await resp.json()
            return f"{data['username']}  Баланс: {data['balance']}, Крутки: {data['spins']}"
    return None

async def player_exists(user_id)->bool:
    #response = request.get(f"{syte_url}/get_stats/{user_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/get_stats/{user_id}") as resp:
        return resp.status == 200

async def get_users_list()->str:
    #response = request.get(f"{syte_url}/get_users_list")
    session = await get_session()
    async with session.get(f"{syte_url}/get_users_list") as resp:
        if resp.status == 200:
            data = await resp.json()
            return data.get("stats",0)
        return "Список пуст, или к нему нет доступа"

###########GET Chats
async def get_chat_rules_str(chat_id):
    #response = request.get(f"{syte_url}/take_data/{chat_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/take_data/{chat_id}") as resp:
        if resp.status == 200:
            data = await  resp.json()

            status_map = {1: "on", 0: "off"}

            result = (f"Название: {data['name']}\n"
                      f"Слоты: {status_map[data['m_slots']]}\n"
                      f"Команды: {status_map[data['m_chat_commands']]}\n"
                      f"Реакции: {status_map[data['m_reactions']]}\n"
                      f"Приветствия: {status_map[data['m_welcome']]}\n"
                      f"Работа: {status_map[data['m_work']]}\n"
                      f"Мин.баланс: {data['min_balance']}")
            return result

        return "Чат не найден"

async def get_chat_rules_dict(chat_id):
    #response = request.get(f"{syte_url}/take_data/{chat_id}")
    session = await get_session()
    async with session.get(f"{syte_url}/take_data/{chat_id}") as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        return None

###########SETChats
async def set_chat_rules(rules: tuple):
    data = {
        "chat_id": rules[0],
        "chat_name": rules[1],
        "m_slots": rules[2],
        "m_chat_commands": rules[3],
        "m_reactions": rules[4],
        "m_welcome": rules[5],
        "m_work": rules[6],
        "min_balance": rules[7]
    }
    session = await get_session()
    async with session.post(f"{syte_url}/save_chats", json=data) as resp:
        await resp.json()

async def change_chat_rules(rules: tuple):
    data = {
        "chat_id": rules[0],
        "m_slots": rules[1],
        "m_chat_commands": rules[2],
        "m_reactions": rules[3],
        "m_welcome": rules[4],
        "m_work": rules[5],
        "min_balance": rules[6]
    }
    session = await get_session()
    async with session.post(f"{syte_url}/change_rules", json=data) as resp:
        return resp.json()




#Update/обновить/ Players/Таблица/ SET/установить/ spin/параметр который изменится/ =?/можно указать параметр в скобках/
#WHERE/поиск строки по параметру/ user_id/параметр для поиска/, {список параметров которые подставятся вместо "?"}
async def check_loot(message: types.Message,user_id, deposit:int):
    if message.dice and message.dice.emoji == casino and not message.forward_from:
        old_balance = await get_balance(user_id)
        rules = await get_chat_rules_dict(message.chat.id)
        min_balance = rules['min_balance'] if rules is not None else -500
        if old_balance <= min_balance :
            return
        new_balance = old_balance-deposit
        new_spins = await get_spins(user_id)+1
        if int(message.dice.value) == 64:
            new_balance += deposit * Coefficients["777"]

        elif int(message.dice.value) == 43:
            new_balance += deposit*Coefficients["lll"]

        elif int(message.dice.value) == 22:
            new_balance += deposit * Coefficients["ggg"]

        elif int(message.dice.value) == 1:
            new_balance += deposit * Coefficients["bbb"]
        await change_balance(user_id, new_balance)
        await change_spins(user_id, new_spins)
    else:
        return


