from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Punteggi iniziali dei giocatori
punteggi = {
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
        for giocatore in punteggi.keys():
            punti_base = int(request.form.get(f"{giocatore}_punti", 0))
            bonus = int(request.form.get(f"{giocatore}_bonus", 0))
            malus = int(request.form.get(f"{giocatore}_malus", 0))
            punteggi[giocatore] += punti_base + bonus - malus
        return redirect(url_for("risultati"))
    return render_template("inserisci.html", giocatori=punteggi.keys())

@app.route("/risultati")
def risultati():
    return render_template("risultati.html", punteggi=punteggi)

if __name__ == "__main__":
    app.run(debug=True)
