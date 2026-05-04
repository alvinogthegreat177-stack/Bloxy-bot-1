import sqlite3

db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

def init_db():
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, verified INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS chats (user TEXT, data TEXT)")
    db.commit()
