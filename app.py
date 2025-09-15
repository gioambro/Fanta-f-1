from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersegreto"  # cambia se vuoi più sicurezza

DB_NAME = "database.db"


# 🔹 Funzione che crea il DB se non esiste
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')

        # inseriamo un utente di test
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user", "1234"))

        conn.commit()
        conn.close()


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
