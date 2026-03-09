import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def init():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    link TEXT,
    send INTEGER,
    status INTEGER,
    lang TEXT)""")
    connection.commit()
    print("[DATABASE] Database created successfully.")

def add_usr(id):
    sql = "INSERT INTO users (user_id, link, send, status, lang) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (id, 'https://google.com/', 0, 1, 'en'))
    connection.commit()
    print(f"[DATABASE] User {id} added successfully.")

def chg_usr(link, send, id):
    sql1 = "UPDATE users SET link = ? WHERE user_id = ?"
    sql2 = "UPDATE users SET send = ? WHERE user_id = ?"
    cursor.execute(sql1, (link, id))
    cursor.execute(sql2, (send, id))
    print(f"[DATABASE] User {id} changed successfully.")
    connection.commit()

def get_link(id):
    sql = "SELECT link FROM users WHERE user_id = ?"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

def get_send(id):
    sql = "SELECT send FROM users WHERE user_id = ?"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

def get_status(id):
    sql = "SELECT status FROM users WHERE user_id = ?"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

def get_lang(id):
    sql = "SELECT lang FROM users WHERE user_id = ?"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

def chk_usr(id):
    sql = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)"
    cursor.execute(sql, (id,))
    return cursor.fetchone()[0]

def usr_list():
    sql = "SELECT user_id FROM users"
    cursor.execute(sql)
    return cursor.fetchall()

def chg_status(id, status):
    sql = "UPDATE users SET status = ? WHERE user_id = ?"
    cursor.execute(sql, (status, id))
    connection.commit()

def chg_lang(id, lang):
    sql = "UPDATE users SET lang = ? WHERE user_id = ?"
    cursor.execute(sql, (lang, id))
    connection.commit()