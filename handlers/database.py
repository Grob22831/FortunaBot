import sqlite3
from handlers.stb import casino, Coefficients
from aiogram import types
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../members.db")
CH_DB_PATH = os.path.join(BASE_DIR, "../../chats.db")


# ------------------- CONNECT -------------------
def connect_db():
    return sqlite3.connect(DB_PATH)


def connect_chats_db():
    return sqlite3.connect(CH_DB_PATH)


# ------------------- MEMBERS -------------------
def add_user(user_id, username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO Players (user_id, username, balance, spins) VALUES (?, ?, ?, ?)',
        (user_id, username, 1000, 0)
    )
    conn.commit()
    conn.close()


def change_balance(user_id, new_balance):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Players SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()


def change_spins(user_id, new_spins):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Players SET spins = ? WHERE user_id = ?", (new_spins, user_id))
    conn.commit()
    conn.close()


def get_balance(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM Players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0


def get_spins(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT spins FROM Players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0


def get_stats(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, balance, spins FROM Players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return f"{row[0]}  Баланс: {row[1]}, Крутки: {row[2]}"
    return None


def get_users_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, balance, spins FROM Players")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "Список пуст, или к нему нет доступа"
    return "\n".join([f"Пользователь: {r[0]}, Баланс: {r[1]}, Крутки:{r[2]}" for r in rows])


def player_exists(user_id) -> bool:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Players WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()
    conn.close()
    return bool(exists)


# ------------------- CHATS -------------------
def set_chat_rules(rules: tuple):
    conn = connect_chats_db()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT OR REPLACE INTO Chats 
           (id, name, m_slots, m_chat_commands, m_reactions, m_welcome, m_work, min_balance)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        rules
    )
    conn.commit()
    conn.close()


def change_chat_rules(rules: tuple):
    conn = connect_chats_db()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE Chats SET
           m_slots = ?, m_chat_commands = ?, m_reactions = ?, m_welcome = ?, m_work = ?, min_balance = ?
           WHERE id = ?''',
        (rules[1], rules[2], rules[3], rules[4], rules[5], rules[6], rules[0])
    )
    conn.commit()
    conn.close()


def get_chat_rules_dict(chat_id):
    conn = connect_chats_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chats WHERE id = ?", (chat_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "m_slots": row[2],
            "m_chat_commands": row[3],
            "m_reactions": row[4],
            "m_welcome": row[5],
            "m_work": row[6],
            "min_balance": row[7]
        }
    return None


def get_chat_rules_str(chat_id):
    rules = get_chat_rules_dict(chat_id)
    if not rules:
        return "Чат не найден"
    status_map = {1: "on", 0: "off"}
    return (
        f"Название: {rules['name']}\n"
        f"Слоты: {status_map[rules['m_slots']]}\n"
        f"Команды: {status_map[rules['m_chat_commands']]}\n"
        f"Реакции: {status_map[rules['m_reactions']]}\n"
        f"Приветствия: {status_map[rules['m_welcome']]}\n"
        f"Работа: {status_map[rules['m_work']]}\n"
        f"Мин.баланс: {rules['min_balance']}"
    )


# ------------------- LOOT -------------------
def check_loot(message: types.Message, user_id, deposit: int):
    if not (message.dice and message.dice.emoji == casino) or message.forward_from:
        return

    old_balance = get_balance(user_id)
    rules = get_chat_rules_dict(message.chat.id)
    min_balance = rules['min_balance'] if rules else -500
    if old_balance <= min_balance:
        return

    new_balance = old_balance - deposit
    new_spins = get_spins(user_id) + 1

    dice_val = int(message.dice.value)
    if dice_val == 64:
        new_balance += deposit * Coefficients["777"]
    elif dice_val == 43:
        new_balance += deposit * Coefficients["lll"]
    elif dice_val == 22:
        new_balance += deposit * Coefficients["ggg"]
    elif dice_val == 1:
        new_balance += deposit * Coefficients["bbb"]

    change_balance(user_id, new_balance)
    change_spins(user_id, new_spins)