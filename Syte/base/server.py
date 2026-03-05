from flask import Flask, request, jsonify, render_template
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../members.db")
CH_DB_PATH  = os.path.join(BASE_DIR, "../../chats.db")
app = Flask(__name__)
def connect_db():
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    return cursor, connect
def connect_chats_db():
    connect = sqlite3.connect(CH_DB_PATH)
    cursor = connect.cursor()
    return cursor, connect

#POST chats
@app.route("/save_chats", methods=["POST"])
def set_rules():
    data = request.json
    chat_id = data.get('chat_id')
    chat_name = data.get('chat_name')
    m_slots = data.get('m_slots')
    m_chat_commands = data.get('m_chat_commands')
    m_reactions = data.get('m_reactions')
    m_welcome = data.get('m_welcome')
    m_work = data.get('m_work')
    min_balance = data.get('min_balance')

    cursor, connect = connect_chats_db()

    cursor.execute("SELECT id FROM Chats WHERE id = ?", (chat_id,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE Chats SET name = ?, m_slots = ?, m_chat_commands = ?, "
            "m_reactions = ?, m_welcome = ?, m_work = ?, min_balance = ? "
            "WHERE id = ?",
            (chat_name, m_slots, m_chat_commands, m_reactions,
             m_welcome, m_work, min_balance, chat_id)
        )
    else:
        cursor.execute(
            "INSERT INTO Chats (id, name, m_slots, m_chat_commands, "
            "m_reactions, m_welcome, m_work, min_balance) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (chat_id, chat_name, m_slots, m_chat_commands,
             m_reactions, m_welcome, m_work, min_balance)
        )

    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})


@app.route("/change_rules", methods=["POST"])
def change_rules():
    data = request.json
    chat_id = data.get('chat_id')
    m_slots = data.get('m_slots')
    m_chat_commands = data.get('m_chat_commands')
    m_reactions = data.get('m_reactions')
    m_welcome = data.get('m_welcome')
    m_work = data.get('m_work')
    min_balance = data.get('min_balance')

    cursor, connect = connect_chats_db()

    cursor.execute(
        "UPDATE Chats SET m_slots = ?, m_chat_commands = ?, m_reactions = ?, "
        "m_welcome = ?, m_work = ?, min_balance = ? WHERE id = ?",
        (m_slots, m_chat_commands, m_reactions,
         m_welcome, m_work, min_balance, chat_id)
    )

    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})
################GET chats
@app.route("/take_data/<int:chat_id>", methods=["GET"])  # добавил параметр в URL
def get_chat_rules(chat_id):  # переименовал функцию
    cursor, connect = connect_chats_db()
    cursor.execute("SELECT * FROM Chats WHERE id = ?", (chat_id,))  # id вместо chat_id
    result = cursor.fetchone()
    connect.close()
    if result:
        return jsonify({
            "id": result[0],
            "name": result[1],
            "m_slots": result[2],
            "m_chat_commands": result[3],
            "m_reactions": result[4],
            "m_welcome": result[5],
            "m_work": result[6],
            "min_balance": result[7]
        })
    return jsonify({"error": "Chat not found"}), 404




################POST members
@app.route("/save", methods=["POST"])
def save_data():
    data = request.json
    user_id = data.get('user_id')
    user_name = data.get('username')
    balance = data.get('balance')
    spins = data.get('spins')

    cursor,connect = connect_db()
    cursor.execute("UPDATE Players SET balance = ?, spins = ? WHERE user_id = ?",
                   (balance, spins, user_id))
    connect.commit()
    connect.close()

    return jsonify({"status": "ok"})


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    balance = data.get('balance')
    cursor, connect = connect_db()
    cursor.execute('INSERT INTO Players (user_id,username,balance, spins) VALUES (?,?,?,?)', (user_id, username,balance,0))
    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})  # добавить эту строку

@app.route("/add_spins", methods=["POST"])
def change_spins():
    data = request.json
    user_id = data.get('user_id')
    new_spins = data.get('new_spins')
    cursor, connect = connect_db()
    cursor.execute("UPDATE Players SET spins =? WHERE user_id = ?",(new_spins, user_id))
    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})  # добавить эту строку

@app.route("/add_balance", methods=["POST"])
def change_balance():
    data = request.json
    user_id = data.get('user_id')
    new_balance = data.get('new_balance')
    cursor, connect = connect_db()
    cursor.execute("UPDATE Players SET balance =? WHERE user_id = ?",(new_balance, user_id))
    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})  # добавить эту строку

@app.route("/clear_users_list", methods=["POST"])
def clear_users_list():
    cursor, connect = connect_db()
    cursor.execute("DELETE FROM Players")
    connect.commit()
    connect.close()
    return jsonify({"status": "ok"})  # добавить эту строку




#GET members
@app.route("/get_spins/<int:user_id>", methods=["GET"])
def get_spins(user_id):
    cursor, connect = connect_db()
    cursor.execute("SELECT spins FROM Players WHERE user_id = ?",( user_id,))
    result =cursor.fetchone()
    connect.commit()
    connect.close()
    if result:
        return jsonify({"spins":result[0]})
    return jsonify({"error": "User not found"}), 404



@app.route("/get_balance/<int:user_id>", methods=["GET"])
def get_balance(user_id):
    cursor, connect = connect_db()
    cursor.execute("SELECT balance FROM Players WHERE user_id = ?",( user_id,))
    result =cursor.fetchone()
    connect.commit()
    connect.close()
    if result:
        return jsonify({"balance":result[0]})
    return jsonify({"error": "User not found"}), 404

@app.route("/get_users_list", methods=["GET"])
def get_users_list():
    cursor, connect = connect_db()
    cursor.execute("SELECT username, balance,spins FROM Players")
    rows = cursor.fetchall()
    result = ""
    for row in rows:
        result += f"Пользователь: {row[0]}, Баланс: {row[1]}, Крутки:{row[2]}\n"
    connect.commit()
    connect.close()
    if result:
        return jsonify({"stats":result})
    return jsonify({"error": "User not found"}), 404


@app.route('/get_stats/<int:user_id>', methods=['GET'])
def get_stats(user_id):
    cursor,connect = connect_db()
    cursor.execute("SELECT username, balance, spins FROM Players WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connect.close()

    if result:
        return jsonify({
            "username": result[0],
            "balance": result[1],
            "spins": result[2]
        })
    return jsonify({"error": "User not found"}), 404

@app.route('/')
def index():
    cursor, connect = connect_db()
    cursor.execute("SELECT username, balance, spins FROM Players")
    users = cursor.fetchall()
    print("USERS:", users)
    connect.close()
    return render_template('syte.html', users=users)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)


