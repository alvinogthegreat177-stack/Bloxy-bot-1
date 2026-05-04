from core.ai_engine import ask_ai
from core.tools import wiki, dictionary

def handle_chat(user, msg):

    t = msg.lower()

    if "define" in t:
        return dictionary(msg)

    if "who is" in t:
        return wiki(msg)

    return ask_ai(msg)
