from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CLASSIFICA_FILE = "classifica.csv"

# Punti ufficiali F1 (solo prime 10 posizioni)
PUNTI_BASE = {
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

# Inizializza file classifica se non esiste
if not os.path.exists(CLASSIFICA_FILE):
    with open(CLASSIFICA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Squadra", "Punti"])


def calcola_punti(partenza, arrivo, giro_veloce, ritiro, sprint):
    punti = 0

    # Punti base per posizione di arrivo
    punti += PUNTI_BASE.get(arrivo, 0)

    # Bonus/malus posizioni
    if arrivo > 0 and partenza > 0:
        differenza = partenza - arrivo
        if differenza > 0:
            punti += differenza * 0.5  # guadagnate
        elif differenza < 0:
            punti += differenza * 0.5  # perse (diventa negativo)

    # Giro veloce
    if giro_veloce:
        punti += 1

    # Sprint
    if sprint:
        punti += 3

    # Ritiro
    if ritiro:
        punti -= 2

    return punti


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        squadra = request.form["squadra"]

        # Pilota 1
        partenza1 = int(request.form.get("partenza1", 0))
        arrivo1 = int(request.form.get("arrivo1", 0))
        giro_veloce1 = "giro_veloce1" in request.form
        ritiro1 = "ritiro1" in request.form
        sprint1 = "sprint1" in request.form
        punti1 = calcola_punti(partenza1, arrivo1, giro_veloce1, ritiro1, sprint1)

        # Pilota 2
        partenza2 = int(request.form.get("partenza2", 0))
        arrivo2 = int(request.form.get("arrivo2", 0))
        giro_veloce2 = "giro_veloce2" in request.form
        ritiro2 = "ritiro2" in request.form
        sprint2 = "sprint2" in request.form
        punti2 = calcola_punti(partenza2, arrivo2, giro_veloce2, ritiro2, sprint2)

        punti_totali = punti1 + punti2

        # Aggiorna classifica
        aggiorna_classifica(squadra, punti_totali)

        return redirect(url_for("risultati"))

    return render_template("inserisci.html")


def aggiorna_classifica(squadra, punti):
    righe = []
    trovato = False

    with open(CLASSIFICA_FILE, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == squadra:
                row[1] = str(float(row[1]) + punti)
                trovato = True
            righe.append(row)

    if not trovato:
        righe.append([squadra, str(punti)])

    with open(CLASSIFICA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Squadra", "Punti"])
        writer.writerows(righe)


@app.route("/risultati")
def risultati():
    classifica = []
    with open(CLASSIFICA_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            classifica.append([row[0], float(row[1])])

    # Ordina per punti
    classifica.sort(key=lambda x: x[1], reverse=True)

    return render_template("risultati.html", classifica=classifica)


if __name__ == "__main__":
    app.run(debug=True)
