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
    return render_template("inserisci.html", giocatori=list(classifica.keys()))

@app.route("/salva", methods=["POST"])
def salva():
    for giocatore in classifica.keys():
        for i in range(1, 3):  # 2 piloti per giocatore
            pilota = request.form.get(f"{giocatore}_pilota{i}")
            if not pilota:
                continue

            griglia = int(request.form.get(f"{giocatore}_pilota{i}_griglia", 0))
            posizione = int(request.form.get(f"{giocatore}_pilota{i}_posizione", 0))

            sprint = request.form.get(f"{giocatore}_pilota{i}_sprint", "no")
            sprint_pos = int(request.form.get(f"{giocatore}_pilota{i}_sprint_pos", 0)) if sprint == "si" else 0

            punti = 0

            # ---- Punti GP ----
            if posizione in punti_gp:
                punti += punti_gp[posizione]

            # ---- Punti Sprint ----
            if sprint == "si" and sprint_pos in punti_sprint:
                punti += punti_sprint[sprint_pos]

            # ---- Bonus ----
            if request.form.get(f"{giocatore}_pilota{i}_pole") == "si":
                punti += 2
            if request.form.get(f"{giocatore}_pilota{i}_fastest_lap"):
                punti += 1
            if request.form.get(f"{giocatore}_pilota{i}_driver_day"):
                punti += 1
            if request.form.get(f"{giocatore}_pilota{i}_fastest_pit"):
                punti += 2
            if request.form.get(f"{giocatore}_pilota{i}_rimonta") == "si":
                punti += 2
            if request.form.get(f"{giocatore}_pilota{i}_pos_guadagnate") == "si" and posizione and griglia and posizione < griglia:
                punti += 0.5 * (griglia - posizione)
            if request.form.get(f"{giocatore}_pilota{i}_vittoria") == "si":
                punti += 3
            if request.form.get(f"{giocatore}_pilota{i}_podio") == "si":
                punti += 2

            # ---- Malus ----
            if request.form.get(f"{giocatore}_pilota{i}_squalifica") == "si":
                punti -= 5
            if request.form.get(f"{giocatore}_pilota{i}_dnf") == "si":
                punti -= 3
            if request.form.get(f"{giocatore}_pilota{i}_pen6") == "si":
                punti -= 4
            if request.form.get(f"{giocatore}_pilota{i}_pen5") == "si":
                punti -= 3
            if request.form.get(f"{giocatore}_pilota{i}_last_place"):
                punti -= 2
            if request.form.get(f"{giocatore}_pilota{i}_q1") == "si":
                punti -= 1
            if request.form.get(f"{giocatore}_pilota{i}_pos_perse") == "si" and posizione and griglia and posizione > griglia and request.form.get(f"{giocatore}_pilota{i}_dnf") == "no":
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
