import os
import requests as request
from aiogram import types
from handlers.stb import casino, Coefficients
from dotenv import load_dotenv



load_dotenv()
syte_url = f"http://{os.getenv("syte_ip")}:5000"



async def add_user(user_id, username):
    data = {"user_id": user_id, "username": username}
    request.post(f"{syte_url}/add_user", json=data)

async def change_spins(user_id,new_spins):
    data = {"user_id": user_id, "new_spins":new_spins}
    request.post(f"{syte_url}/add_spins", json=data)

async def change_balance(user_id,new_balance):
    data = {"user_id": user_id, "new_balance":new_balance}
    request.post(f"{syte_url}/add_balance", json=data)
async def clear_users_list():
    request.post(f"{syte_url}/clear_users_list")




#############  GET
async def get_balance(user_id):
    response = request.get(f"{syte_url}/get_balance/{user_id}")
    if response.status_code == 200:
        return response.json().get("balance", 0)
    return 0

async def get_spins(user_id):
    response = request.get(f"{syte_url}/get_spins/{user_id}")
    if response.status_code == 200:
        return response.json().get("spins", 0)
    return 0

async def get_stats(user_id):
    response = request.get(f"{syte_url}/get_stats/{user_id}")
    if response.status_code == 200:
        data = response.json()
        return f"{data['username']}  Баланс: {data['balance']}, Крутки: {data['spins']}"
    return None

async def player_exists(user_id):
    response = request.get(f"{syte_url}/get_stats/{user_id}")
    return response.status_code == 200

async def get_users_list()->str:
    response = request.get(f"{syte_url}/get_users_list")
    if response.status_code == 200:
        return response.json().get("stats",0)
    return "Список пуст, или к нему нет доступа"


#Update/обновить/ Players/Таблица/ SET/установить/ spin/параметр который изменится/ =?/можно указать параметр в скобках/
#WHERE/поиск строки по параметру/ user_id/параметр для поиска/, {список параметров которые подставятся вместо "?"}
async def check_loot(message: types.Message,user_id, deposit:int):
    if message.dice and message.dice.emoji == casino and not message.forward_from:
        new_balance = await get_balance(user_id)-deposit
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


