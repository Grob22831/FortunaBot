from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
def connect_db():
    connect = sqlite3.connect('../../members.db')
    cursor = connect.cursor()
    return cursor, connect
def init_db():
    conn = sqlite3.connect('../../members.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 0,
            spins INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

#POST
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
    cursor, connect = connect_db()
    cursor.execute('INSERT INTO Players (user_id,username,balance, spins) VALUES (?,?,?,?)', (user_id, username,0,0))
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




#GET
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



if __name__ == '__main__':
    #init_db()
    app.run(host='0.0.0.0', port=5000)


