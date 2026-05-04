import sqlite3
import json

db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

def save_message(user, message, reply):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user TEXT,
            data TEXT
        )
    """)
    db.commit()

    cur.execute("SELECT data FROM memory WHERE user=?", (user,))
    row = cur.fetchone()

    history = json.loads(row[0]) if row else []

    history.append({"user": message, "ai": reply})

    if row:
        cur.execute("UPDATE memory SET data=? WHERE user=?", (json.dumps(history), user))
    else:
        cur.execute("INSERT INTO memory VALUES (?,?)", (user, json.dumps(history)))

    db.commit()


def load_memory(user):
    cur.execute("SELECT data FROM memory WHERE user=?", (user,))
    row = cur.fetchone()

    if not row:
        return []

    return json.loads(row[0])
