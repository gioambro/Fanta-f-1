from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersegreto"  # cambialo con qualcosa di più sicuro

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Login (esempio minimo)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # qui puoi aggiungere il controllo su un database o utenti fissi
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Credenziali errate")
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Admin page
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("admin.html")

# Inserisci (GET mostra form, POST gestisce dati)
@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form.get("nome")
        valore = request.form.get("valore")
        # per ora stampiamo solo in console, poi puoi salvarli in DB
        print(f"Ricevuto: Nome={nome}, Valore={valore}")
        return render_template("inserisci.html", message="Dati salvati!")

    return render_template("inserisci.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
