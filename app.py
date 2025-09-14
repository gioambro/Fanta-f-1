from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Classifica iniziale
punteggi = {
    "Alfarumeno": 0,
    "Stalloni": 0,
    "WC in Geriatria": 0,
    "Strolling Around": 0,
    "Spartaboyz": 0,
    "Vodkaredbull": 0
}

# Punti FIA standard
punti_fia = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        for team in punteggi.keys():
            totale_team = 0
            for pilota in [1, 2]:
                griglia = int(request.form.get(f"{team}_p{pilota}_griglia", 0))
                arrivo = int(request.form.get(f"{team}_p{pilota}_arrivo", 0))
                sprint = request.form.get(f"{team}_p{pilota}_sprint", "No")
                bonus = int(request.form.get(f"{team}_p{pilota}_bonus", 0))
                malus = int(request.form.get(f"{team}_p{pilota}_malus", 0))

                # Punti base FIA
                base = punti_fia.get(arrivo, 0)

                # Sprint -> metà punti
                if sprint == "Si":
                    base = base / 2

                # Posizioni guadagnate/perse
                delta = griglia - arrivo
                if delta > 0:
                    extra = delta * 1       # +1 punto a posizione guadagnata
                else:
                    extra = delta * 0.5     # -0.5 punti a posizione persa

                punti_pilota = base + extra + bonus - malus
                totale_team += punti_pilota

            punteggi[team] += totale_team

        return redirect(url_for("risultati"))

    return render_template("inserisci.html", squadre=punteggi.keys())

@app.route("/risultati")
def risultati():
    return render_template("risultati.html", punteggi=punteggi)

if __name__ == "__main__":
    app.run(debug=True)
