from core.tools import wiki, dictionary, tavily, news, wolfram
from core.ai_engine import ask_ai

# ---------------- TOOL ROUTER ----------------
def use_tools(msg):
    t = msg.lower()

    # dictionary / meaning
    if "define" in t or "meaning" in t:
        return dictionary(msg)

    # wikipedia facts
    if "who is" in t or "what is" in t:
        return wiki(msg)

    # news
    if "news" in t or "latest" in t:
        return news()

    # web search
    if "search" in t:
        return tavily(msg)

    # math / scientific (wolfram placeholder)
    if "solve" in t or "=" in t:
        return wolfram(msg)

    return None


# ---------------- MAIN CHAT HANDLER ----------------
def handle_chat(user, msg):

    # STEP 1: try tools first
    tool_result = use_tools(msg)

    # STEP 2: if tool gives answer, return it
    if tool_result:
        return tool_result

    # STEP 3: otherwise use AI brain
    return ask_ai(msg)
