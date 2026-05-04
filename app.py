from flask import Flask, request, jsonify, render_template_string, session
from core.db import init_db
from core.auth import signup, login, logout, get_user
from core.chat import handle_chat

app = Flask(__name__)
app.secret_key = "dev-key"

init_db()

# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Chat</title>
<style>
body{margin:0;font-family:Arial;background:#0b0f1a;color:white;display:flex;height:100vh;}
.sidebar{width:260px;background:#111827;padding:10px;}
.chat{flex:1;display:flex;flex-direction:column;}
.box{flex:1;overflow:auto;padding:10px;}
.msg{padding:8px;margin:6px;border-radius:8px;max-width:70%;}
.user{background:#2563eb;margin-left:auto;}
.ai{background:#1f2937;}
.input{display:flex;padding:10px;background:#111827;}
input{flex:1;padding:10px;}
button{padding:10px;background:#2563eb;color:white;border:none;}
.account{position:fixed;bottom:10px;left:10px;background:#1f2937;padding:8px;border-radius:8px;}
</style>
</head>
<body>

<div class="sidebar">
<h3>Account</h3>
<input id="u" placeholder="username">
<input id="p" type="password" placeholder="password">
<button onclick="signup()">Signup</button>
<button onclick="login()">Login</button>
<button onclick="logout()">Logout</button>
</div>

<div class="chat">
<div class="box" id="box"></div>
<div class="input">
<input id="msg" placeholder="Type..." onkeypress="if(event.key==='Enter') send()">
<button onclick="send()">Send</button>
</div>
</div>

<div class="account" id="acc">Guest</div>

<script>
let user="Guest";

async function refresh(){
 let r=await fetch("/me");
 let d=await r.json();
 user=d.name;
 acc.innerText=user + (d.verified ? " 🟠✔" : "");
}

async function signup(){
 await fetch("/signup",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({u:u.value,p:p.value})});
}

async function login(){
 await fetch("/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({u:u.value,p:p.value})});
 refresh();
}

async function logout(){
 await fetch("/logout");
 refresh();
}

async function send(){
 let m=msg.value;
 if(!m)return;

 box.innerHTML+=`<div class="msg user">${user}: ${m}</div>`;
 msg.value="";

 let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({m})});
 let d=await r.json();

 box.innerHTML+=`<div class="msg ai">${d.reply}</div>`;
}

refresh();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

# ---------------- AUTH ----------------
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

# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    user = get_user()["name"]
    msg = request.json["m"]
    return jsonify({"reply": handle_chat(user, msg)})

if __name__ == "__main__":
    app.run(debug=True)
