import wikipedia
import requests
import os

TAVILY_KEY = os.getenv("TAVILY_API_KEY", "")
NEWS_KEY = os.getenv("NEWS_API_KEY", "")

# ---------------- Wikipedia ----------------
def wiki(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return None

# ---------------- Dictionary ----------------
def dictionary(word):
    try:
        r = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        ).json()
        return r[0]["meanings"][0]["definitions"][0]["definition"]
    except:
        return None

# ---------------- Tavily (Web Search) ----------------
def tavily(query):
    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": TAVILY_KEY, "query": query}
        ).json()
        return r.get("results", [{}])[0].get("content")
    except:
        return None

# ---------------- News ----------------
def news():
    try:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_KEY}"
        ).json()

        return "\n".join([a["title"] for a in r.get("articles", [])[:5]])
    except:
        return None

# ---------------- Wolfram (placeholder) ----------------
def wolfram(query):
    return None
