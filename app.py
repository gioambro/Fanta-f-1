from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Squadre e piloti (puoi modificare i nomi a piacere)
squadre = {
    "Alfarumeno": ["Pilota 1", "Pilota 2"],
    "WC in Geriatria": ["Pilota 1", "Pilota 2"]
}

risultati = {}

# Funzione di calcolo punteggi
def calcola_punti(form, squadra, pilota):
    griglia = int(form.get(f"griglia_{squadra}_{pilota}"))
    posizione = int(form.get(f"posizione_{squadra}_{pilota}"))
    sprint = form.get(f"sprint_{squadra}_{pilota}") == "si"

    punti = 0

    if not sprint:
        # BONUS
        if form.get(f"pole_{squadra}_{pilota}") == "si":
            punti += 2
        if form.get(f"giroveloce_{squadra}_{pilota}") == "si":
            punti += 1
        if form.get(f"dotd_{squadra}_{pilota}") == "si":
            punti += 1
        if form.get(f"pitstop_{squadra}_{pilota}") == "si":
            punti += 2
        if griglia >= 19 and posizione <= 10:
            punti += 2
        if posizione < griglia:
            punti += (griglia - posizione) * 0.5
        if posizione == 1:
            punti += 3
        elif posizione in [2, 3]:
            punti += 2

        # MALUS
        if form.get(f"squalifica_{squadra}_{pilota}") == "si":
            punti -= 5
        if form.get(f"dnf_{squadra}_{pilota}") == "si":
            punti -= 3
        else:
            if form.get(f"penalita6_{squadra}_{pilota}") == "si":
                punti -= 4
            if form.get(f"penalita5_{squadra}_{pilota}") == "si":
                punti -= 3
            if form.get(f"ultimo_{squadra}_{pilota}") == "si":
                punti -= 2
            if form.get(f"q1_{squadra}_{pilota}") == "si":
                punti -= 1
            if posizione > griglia:
                punti -= (posizione - griglia) * 0.5

    return punti


@app.route("/")
def index():
    return render_template("index.html", squadre=squadre)


@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    global risultati
    if request.method == "POST":
        risultati = {}
        for squadra in squadre:
            risultati[squadra] = []
            for pilota in range(1, 3):
                punti = calcola_punti(request.form, squadra, pilota)
                risultati[squadra].append(punti)
        return redirect(url_for("risultati_view"))
    return render_template("inserisci.html", squadre=squadre)


@app.route("/risultati")
def risultati_view():
    totali = {s: sum(risultati.get(s, [0, 0])) for s in squadre}
    return render_template("risultati.html", risultati=risultati, totali=totali)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
