import sqlite3
conn = sqlite3.connect('members.db')
cursor = conn.cursor()
import  types

#искать в таблице players по user_id
async def player_exists(user_id):
    cursor.execute('SELECT * FROM Players WHERE user_id = ?', (user_id,))
    return cursor.fetchone() is not None


#Вставить новую запись в таблицу players (нужные поля)
async def add_user(user_id, username ):
    cursor.execute('INSERT INTO Players (user_id,username,balance) VALUES (?,?,?)',(user_id,username,0))
    conn.commit()

async def get_users_list()->str:
    cursor.execute("SELECT username, balance FROM Players")
    rows = cursor.fetchall()  # возвращает список кортежей
    string = ""
    for row in rows:
        string += f"Пользователь: {row[0]}, Баланс: {row[1]}\n"
    return string

async def get_user_stats(user_id)->str:
    cursor.execute("SELECT username, balance,spins FROM Players WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()  # возвращает список кортежей
    string = ""
    for row in rows:
        string += f" {row[0]}, Баланс: {row[1]}, Крутки: {row[2]}\n"
    return string


async def clear_user_list():
    cursor.execute("DELETE FROM Players")
    conn.commit()

async def get_balance(user_id)->int:
    cursor.execute('SELECT balance FROM Players WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()
    return balance[0] if balance else 0

async def get_spins(user_id)->int:
    cursor.execute("SELECT spins FROM Players WHERE user_id = ?", (user_id,))
    spins = cursor.fetchone()
    return spins[0]

async def add_spin(user_id,new_spins):
    cursor.execute("UPDATE Players SET spins = ? WHERE user_id = ?",(new_spins,user_id))
    conn.commit()
async def add_balance(user_id,new_balance):
    cursor.execute("UPDATE Players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()