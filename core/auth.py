from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from core.db import cur, db

OWNER = "aTg"

def signup(u, p):
    if u == OWNER:
        return False

    cur.execute(
        "INSERT INTO users VALUES (?,?,?)",
        (u, generate_password_hash(p), 0)
    )
    db.commit()
    return True


def login(u, p):
    cur.execute("SELECT password FROM users WHERE username=?", (u,))
    row = cur.fetchone()

    if row and check_password_hash(row[0], p):
        session["user"] = u
        return True
    return False


def logout():
    session.pop("user", None)


def get_user():
    u = session.get("user")
    if not u:
        return {"name": "Guest", "verified": False}

    return {
        "name": u,
        "verified": u == OWNER
    }
