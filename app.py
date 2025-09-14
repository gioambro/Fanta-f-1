from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# classifica generale
classifica_generale = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# punteggi sprint
sprint_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}

# calcolo punteggio totale
def calcola_punteggio(dati):
    punti = 0

    # Sprint
    if dati.get("sprint") == "si" and dati.get("posizione_sprint"):
        pos = int(dati["posizione_sprint"])
        if pos in sprint_points:
            punti += sprint_points[pos]

    # Vittoria/podio automatici da posizione GP
    pos_finale = int(dati["posizione_finale"])
    griglia = int(dati["griglia"])

    if pos_finale == 1:
        punti += 3  # vittoria
    elif pos_finale in [2, 3]:
        punti += 2  # podio

    # differenza posizioni
    if dati.get("dnf") != "si":  # se non è DNF
        diff = griglia - pos_finale
        if diff > 0:
            punti += diff * 0.5
        elif diff < 0:
            punti += diff * 0.5

    # bonus sì/no
    if dati.get("pole") == "si":
        punti += 2
    if dati.get("giro_veloce") == "si":
        punti += 1
    if dati.get("driver_day") == "si":
        punti += 1
    if dati.get("pit_stop") == "si":
        punti += 2
    if dati.get("ultime_file") == "si":
        punti += 2

    # malus sì/no
    if dati.get("squalifica") == "si":
        punti -= 5
    if dati.get("dnf") == "si":
        punti -= 3
    if dati.get("penalita6") == "si":
        punti -= 4
    if dati.get("penalita5") == "si":
        punti -= 3
    if dati.get("ultimo") == "si" and dati.get("dnf") != "si":
        punti -= 2
    if dati.get("no_q1") == "si":
        punti -= 1

    return punti


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        giocatore = request.form["giocatore"]
        punti = calcola_punteggio(request.form)
        classifica_generale[giocatore] += punti
        return redirect(url_for("risultati", giocatore=giocatore, punti=punti))
    return render_template("inserisci.html", giocatori=classifica_generale.keys())


@app.route("/risultati")
def risultati():
    giocatore = request.args.get("giocatore")
    punti = request.args.get("punti")
    return render_template("risultati.html",
                           giocatore=giocatore,
                           punti=punti,
                           classifica=sorted(classifica_generale.items(),
                                             key=lambda x: x[1],
                                             reverse=True))


if __name__ == "__main__":
    app.run(debug=True)
