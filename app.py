from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cambialo in produzione!

DB_FILE = "users.db"

# -----------------------------
# Utility database
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

# -----------------------------
# Dizionario piloti per giocatore
# -----------------------------
piloti_giocatori = {
    "Alfarumeno": ["Norris", "Tsunoda", "Colapinto"],
    "Strolling Around": ["Russell", "Gasly", "Antonelli"],
    "Stalloni": ["Piastri", "Lawson", "Ocon"],
    "WC in Geriatria": ["Alonso", "Hamilton", "Hadjar"],
    "Vodkaredbull": ["Verstappen", "Sainz", "Bortoleto"],
    "Spartaboyz": ["Leclerc", "Bearman", "Albon"]
}

# -----------------------------
# Rotte di autenticazione
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash("Login effettuato con successo!", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenziali errate!", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout effettuato", "info")
    return redirect(url_for("login"))

# -----------------------------
# Cambio password
# -----------------------------
@app.route("/cambia_password", methods=["GET", "POST"])
def cambia_password():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        old = request.form["old_password"]
        new = request.form["new_password"]

        user = get_user(session["username"])
        if user and check_password_hash(user["password"], old):
            conn = get_db()
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = ? WHERE username = ?",
                        (generate_password_hash(new), session["username"]))
            conn.commit()
            conn.close()
            flash("Password aggiornata con successo!", "success")
            return redirect(url_for("index"))
        else:
            flash("Password attuale errata", "danger")

    return render_template("change_password.html")

# -----------------------------
# Home e pannello admin
# -----------------------------
@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM formazioni")
    formazioni = cur.fetchall()
    conn.close()
    return render_template("index.html", user=session.get("username"), role=session.get("role"), formazioni=formazioni)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("role") != "admin":
        flash("Accesso negato!", "danger")
        return redirect(url_for("index"))

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        action = request.form["action"]

        if action == "add":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        (username, generate_password_hash(password), role))
            conn.commit()
            flash("Utente aggiunto!", "success")

        elif action == "delete":
            username = request.form["username"]
            if username != "admin":  # Non eliminare admin
                cur.execute("DELETE FROM users WHERE username = ?", (username,))
                conn.commit()
                flash("Utente eliminato!", "warning")

        elif action == "reset":
            username = request.form["username"]
            newpass = request.form["new_password"]
            cur.execute("UPDATE users SET password = ? WHERE username = ?",
                        (generate_password_hash(newpass), username))
            conn.commit()
            flash("Password resettata!", "info")

    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()
    conn.close()

    return render_template("admin.html", users=users)

# -----------------------------
# Inserimento piloti
# -----------------------------
@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if "username" not in session:
        return redirect(url_for("login"))

    user = session["username"]

    if user not in piloti_giocatori:
        flash("Il tuo account non ha piloti assegnati!", "danger")
        return redirect(url_for("index"))

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        pilota1 = request.form.get("pilota1")
        pilota2 = request.form.get("pilota2")

        if pilota1 == pilota2:
            flash("❌ Devi scegliere due piloti diversi!", "danger")
            return redirect(url_for("inserisci"))

        # Salva o aggiorna la formazione
        cur.execute("""
            INSERT INTO formazioni (username, pilota1, pilota2)
            VALUES (?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET pilota1=excluded.pilota1, pilota2=excluded.pilota2
        """, (user, pilota1, pilota2))
        conn.commit()

        flash(f"✅ Formazione aggiornata: {pilota1} e {pilota2}", "success")
        return redirect(url_for("index"))

    # Recupera eventuale formazione salvata
    cur.execute("SELECT pilota1, pilota2 FROM formazioni WHERE username = ?", (user,))
    formazione = cur.fetchone()
    conn.close()

    return render_template("inserisci.html", user=user, piloti=piloti_giocatori[user], formazione=formazione)

# -----------------------------
# Avvio
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
