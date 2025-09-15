from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersegreto"
DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

    # se il DB è vuoto, inseriamo utenti di test
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user", "1234"))

    conn.commit()
    conn.close()


@app.before_request
def before_request():
    # assicura che il DB esista prima di ogni richiesta
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "❌ Credenziali errate"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"✅ Benvenuto, {session['username']}! <br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
