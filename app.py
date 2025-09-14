from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Classifica parziale dopo 16 gare
giocatori = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        for giocatore in giocatori.keys():
            punti_base = float(request.form.get(f"{giocatore}_punti", 0))
            pos_guadagnate = int(request.form.get(f"{giocatore}_pos_guadagnate", 0))
            pos_perse = int(request.form.get(f"{giocatore}_pos_perse", 0))
            bonus = float(request.form.get(f"{giocatore}_bonus", 0))
            malus = float(request.form.get(f"{giocatore}_malus", 0))

            totale = (
                punti_base +
                pos_guadagnate * 0.5 +
                pos_perse * -0.5 +
                bonus +
                malus
            )
            giocatori[giocatore] += totale

        return redirect(url_for("risultati"))

    return render_template("inserisci.html", giocatori=giocatori.keys())

@app.route("/risultati")
def risultati():
    return render_template("risultati.html", giocatori=giocatori)
