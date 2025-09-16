from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cambiala con una stringa a caso per sicurezza

DB_NAME = "fanta.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT driver1, driver2, driver3 FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    drivers = []
    if row:
        drivers = [row["driver1"], row["driver2"], row["driver3"]]

    return render_template("index.html", username=username, drivers=drivers)

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
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenziali non valide")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
