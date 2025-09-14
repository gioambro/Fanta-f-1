import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

DB_FILE = "users.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 👈 fondamentale per accedere con f["username"]
    return conn


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM formazioni")
        formazioni = cur.fetchall()
    except sqlite3.OperationalError:
        # Se la tabella non esiste ancora
        formazioni = []

    conn.close()

    return render_template(
        "index.html",
        user=session.get("username"),
        role=session.get("role"),
        formazioni=formazioni,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("index"))
        else:
            return "❌ Username o password errati"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
