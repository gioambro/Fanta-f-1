from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Punteggi base GP
punti_gp = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}

# Punteggi Sprint
punti_sprint = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}

# Classifica iniziale
classifica = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# Archivio risultati
risultati = []

@app.route("/")
def index():
    return render_template("index.html", classifica=classifica)

@app.route("/inserisci")
def inserisci():
    return render_template("inserisci.html")

@app.route("/salva", methods=["POST"])
def salva():
    giocatore = request.form["giocatore"]
    pilota = request.form["pilota"]

    griglia = int(request.form.get("griglia", 0))
    posizione = int(request.form.get("posizione", 0))

    sprint = request.form.get("sprint", "no")
    sprint_pos = int(request.form.get("sprint_pos", 0)) if sprint == "si" else 0

    punti = 0

    # ---- Punti GP ----
    if posizione in punti_gp:
        punti += punti_gp[posizione]

    # ---- Punti Sprint ----
    if sprint == "si" and sprint_pos in punti_sprint:
        punti += punti_sprint[sprint_pos]

    # ---- Bonus ----
    if request.form.get("pole") == "si":
        punti += 2
    if request.form.get("fastest_lap"):
        punti += 1
    if request.form.get("driver_day"):
        punti += 1
    if request.form.get("fastest_pit"):
        punti += 2
    if request.form.get("rimonta") == "si":
        punti += 2
    if request.form.get("pos_guadagnate") == "si" and posizione and griglia and posizione < griglia:
        punti += 0.5 * (griglia - posizione)
    if request.form.get("vittoria") == "si":
        punti += 3
    if request.form.get("podio") == "si":
        punti += 2

    # ---- Malus ----
    if request.form.get("squalifica") == "si":
        punti -= 5
    if request.form.get("dnf") == "si":
        punti -= 3
    if request.form.get("pen6") == "si":
        punti -= 4
    if request.form.get("pen5") == "si":
        punti -= 3
    if request.form.get("last_place"):
        punti -= 2
    if request.form.get("q1") == "si":
        punti -= 1
    if request.form.get("pos_perse") == "si" and posizione and griglia and posizione > griglia and request.form.get("dnf") == "no":
        punti -= 0.5 * (posizione - griglia)

    # Aggiorna classifica
    classifica[giocatore] += punti

    # Salva risultato singolo
    risultati.append({
        "giocatore": giocatore,
        "pilota": pilota,
        "punti": punti,
        "posizione": posizione,
        "griglia": griglia,
        "sprint": sprint_pos
    })

    return redirect(url_for("risultati_page"))

@app.route("/risultati")
def risultati_page():
    return render_template("risultati.html", risultati=risultati)

if __name__ == "__main__":
    app.run(debug=True)
