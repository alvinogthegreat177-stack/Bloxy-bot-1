import wikipedia
import requests
import os

def wiki(q):
    try:
        return wikipedia.summary(q, sentences=2)
    except:
        return None

def dictionary(word):
    try:
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
        return r[0]["meanings"][0]["definitions"][0]["definition"]
    except:
        return None

def tavily(q):
    return None  # placeholder (needs API key)

def news():
    return "News API not configured"

def wolfram(q):
    return None
