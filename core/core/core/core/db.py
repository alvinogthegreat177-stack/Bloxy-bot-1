import sqlite3

db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT,
        verified INT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        chat_id TEXT,
        user TEXT,
        title TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        chat_id TEXT,
        user TEXT,
        role TEXT,
        content TEXT
    )
    """)

    db.commit()
