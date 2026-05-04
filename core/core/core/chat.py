import uuid
from core.ai_engine import ask_ai
from core.tools import wiki, dictionary, tavily, news, wolfram
from core.db import cur, db


def create_chat(user):
    chat_id = str(uuid.uuid4())

    cur.execute(
        "INSERT INTO chats VALUES (?,?,?)",
        (chat_id, user, "New Chat")
    )
    db.commit()

    return chat_id


def get_chats(user):
    cur.execute("SELECT chat_id, title FROM chats WHERE user=?", (user,))
    return cur.fetchall()


def save_message(chat_id, user, role, content):
    cur.execute(
        "INSERT INTO messages VALUES (?,?,?,?)",
        (chat_id, user, role, content)
    )
    db.commit()


def route_tools(msg):
    t = msg.lower()

    if "define" in t:
        return dictionary(msg)

    if "who is" in t or "what is" in t:
        return wiki(msg)

    if "news" in t:
        return news()

    if "search" in t:
        return tavily(msg)

    if "solve" in t or "=" in t:
        return wolfram(msg)

    return None


def handle_chat(user, chat_id, msg):

    # STEP 1: tools first
    tool = route_tools(msg)

    if tool:
        save_message(chat_id, user, "user", msg)
        save_message(chat_id, user, "assistant", tool)
        return tool

    # STEP 2: AI brain
    reply = ask_ai(msg)

    save_message(chat_id, user, "user", msg)
    save_message(chat_id, user, "assistant", reply)

    return reply
