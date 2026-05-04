import os
from flask import Flask, request, jsonify, render_template_string, session

from core.db import init_db
from core.auth import signup, login, logout, get_user
from core.chat import handle_chat, create_chat, get_chats

app = Flask(__name__)

# 🔐 secret key (required for sessions)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# 🧠 initialize database
init_db()

# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI Chat</title>

<style>
body{margin:0;font-family:Arial;display:flex;height:100vh;background:#0b0f1a;color:white;}
.sidebar{width:280px;background:#111827;padding:10px;display:flex;flex-direction:column;}
.newchat{padding:10px;background:#2563eb;border:none;color:white;border-radius:6px;cursor:pointer;margin-bottom:10px;}
.chatlist{flex:1;overflow-y:auto;}
.chatitem{padding:10px;margin:5px 0;background:#1f2937;border-radius:6px;cursor:pointer;}
.chatitem:hover{background:#374151;}

.main{flex:1;display:flex;flex-direction:column;}
.messages{flex:1;overflow-y:auto;padding:15px;}
.msg{padding:10px;margin:6px;border-radius:10px;max-width:70%;white-space:pre-wrap;}
.user{background:#2563eb;margin-left:auto;}
.ai{background:#1f2937;}

.inputbar{display:flex;padding:10px;background:#111827;}
input{flex:1;padding:12px;border:none;border-radius:6px;outline:none;}
button{padding:12px;margin-left:8px;background:#2563eb;color:white;border:none;border-radius:6px;cursor:pointer;}

.account{
position:fixed;
bottom:10px;
left:10px;
background:#1f2937;
padding:10px;
border-radius:8px;
}
</style>
</head>

<body>

<div class="sidebar">
<button class="newchat" onclick="newChat()">+ New Chat</button>
<div class="chatlist" id="chatlist"></div>
</div>

<div class="main">
<div class="messages" id="messages"></div>

<div class="inputbar">
<input id="input" placeholder="Type..." onkeypress="if(event.key==='Enter') send()">
<button onclick="send()">Send</button>
</div>
</div>

<div class="account" id="account">Guest</div>

<script>

let currentChat = null;
let user = "Guest";

/* ---------------- BADGE ---------------- */
function badge(){
return `
<svg width="14" height="14" viewBox="0 0 24 24" fill="#f97316">
<path d="M12 0l3 3 4-1 1 4 4 3-3 3 1 4-4 1-3 4-3-4-4-1 1-4-3-3 4-3 1-4 4 1z"/>
</svg>`;
}

/* ---------------- USER ---------------- */
async function loadUser(){
let r = await fetch("/me");
let d = await r.json();

user = d.name;
account.innerHTML = user + (d.verified ? " " + badge() : "");
}

/* ---------------- CHATS ---------------- */
async function loadChats(){
let r = await fetch("/chats");
let data = await r.json();

chatlist.innerHTML = "";

data.forEach(c=>{
let div = document.createElement("div");
div.className="chatitem";
div.innerText=c[1];
div.onclick=()=>switchChat(c[0]);
chatlist.appendChild(div);
});
}

/* ---------------- NEW CHAT ---------------- */
async function newChat(){
let r = await fetch("/new_chat");
let d = await r.json();

currentChat = d.chat_id;
messages.innerHTML = "";

loadChats();
}

/* ---------------- SWITCH CHAT ---------------- */
function switchChat(id){
currentChat = id;
messages.innerHTML = "";
}

/* ---------------- SEND ---------------- */
async function send(){

if(!currentChat){
await newChat();
}

let text = input.value;
if(!text) return;

add("You: " + text, "user");
input.value = "";

let r = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
chat_id: currentChat,
m: text
})
});

let d = await r.json();

add("AI: " + d.reply, "ai");
}

/* ---------------- UI ---------------- */
function add(text, cls){
let div = document.createElement("div");
div.className="msg "+cls;
div.innerText=text;
messages.appendChild(div);
messages.scrollTop = messages.scrollHeight;
}

/* ---------------- INIT ---------------- */
loadUser();
loadChats();

</script>

</body>
</html>
"""

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/signup", methods=["POST"])
def route_signup():
    d = request.json
    return jsonify({"ok": signup(d["u"], d["p"])})

@app.route("/login", methods=["POST"])
def route_login():
    d = request.json
    return jsonify({"ok": login(d["u"], d["p"])})

@app.route("/logout")
def route_logout():
    logout()
    return jsonify({"ok": True})

@app.route("/me")
def me():
    return jsonify(get_user())

@app.route("/new_chat")
def new_chat():
    user = get_user()["name"]
    return jsonify({"chat_id": create_chat(user)})

@app.route("/chats")
def chats():
    user = get_user()["name"]
    return jsonify(get_chats(user))

@app.route("/chat", methods=["POST"])
def chat():
    user = get_user()["name"]

    data = request.json
    chat_id = data["chat_id"]
    msg = data["m"]

    reply = handle_chat(user, chat_id, msg)

    return jsonify({"reply": reply})

# ---------------- PRODUCTION SAFE START ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
