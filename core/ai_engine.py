from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

def ask_ai(msg):
    try:
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful ChatGPT-style assistant."},
                {"role": "user", "content": msg}
            ]
        )

        return res.choices[0].message.content

    except:
        return "⚠️ AI temporarily unavailable"
