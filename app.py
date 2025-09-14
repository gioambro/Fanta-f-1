from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File di salvataggio
NOMI_FILE = "nomi_giocatori.json"
STORICO_FILE = "storico.json"

# Nomi e punteggi iniziali (se i file non esistono)
giocatori_iniziali = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# --- Funzioni di supporto ---
def carica_classifica():
    if os.path.exists(STORICO_FILE):
        with open(STORICO_FILE, "r") as f:
            return json.load(f)
    else:
        return giocatori_iniziali.copy()

def salva_classifica(classifica):
    with open(STORICO_FILE, "w") as f:
        json.dump(classifica, f)

# Regole calcolo punti GP
def calcola_punti(dati):
    punti = 0
    posizione = dati.get("posizione")
    griglia = dati.get("griglia")

    try:
        posizione = int(posizione) if posizione else None
        griglia = int(griglia) if griglia else None
    except ValueError:
        posizione, griglia = None, None

    # Bonus automatici per posizione finale
    if posizione == 1:
        punti += 3  # vittoria
    elif posizione in [2, 3]:
        punti += 2  # podio

    # Variazioni rispetto alla griglia
    if posizione and griglia:
        diff = griglia - posizione
        if diff > 0:
            punti += diff * 0.5  # posizioni guadagnate
        elif diff < 0:
            punti += diff * 0.5  # posizioni perse (negativi)

    # Bonus selezionati manualmente
    bonus = dati.getlist("bonus")
    if "pole" in bonus:
        punti += 2
    if "giro_veloce" in bonus:
        punti += 1
    if "driver_day" in bonus:
        punti += 1
    if "pitstop" in bonus:
        punti += 2
    if "ultime_file_punti" in bonus:
        punti += 2

    # Malus selezionati manualmente
    malus = dati.getlist("malus")
    if "squalifica" in malus:
        punti -= 5
    if "dnf" in malus:
        punti -= 3
    if "penalita6" in malus:
        punti -= 4
    if "penalita5" in malus:
        punti -= 3
    if "ultimo" in malus:
        punti -= 2
    if "no_q1" in malus:
        punti -= 1

    # Sprint Race (solo se selezionata)
    if dati.get("sprint") == "si":
        sprint_pos = dati.get("sprint_posizione")
        try:
            sprint_pos = int(sprint_pos)
            if 1 <= sprint_pos <= 8:
                punti += 9 - sprint_pos  # 1°=8 pt, 2°=7 pt, ..., 8°=1 pt
        except (TypeError, ValueError):
            pass

    return punti

# --- Rotte Flask ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    classifica = carica_classifica()
    if request.method == "POST":
        punteggi_giornata = {}

        for giocatore in classifica.keys():
            dati = request.form.getlist(giocatore + "_data")
            # request.form arriva piatto → recuperiamo i singoli campi
            dati_dict = {
                "posizione": request.form.get(f"{giocatore}_posizione"),
                "griglia": request.form.get(f"{giocatore}_griglia"),
                "bonus": request.form.getlist(f"{giocatore}_bonus"),
                "malus": request.form.getlist(f"{giocatore}_malus"),
                "sprint": request.form.get(f"{giocatore}_sprint"),
                "sprint_posizione": request.form.get(f"{giocatore}_sprint_posizione")
            }

            punti = calcola_punti(dati_dict)
            punteggi_giornata[giocatore] = punti
            classifica[giocatore] += punti  # aggiorna la classifica generale

        salva_classifica(classifica)
        return render_template("risultato.html",
                               giornata=punteggi_giornata,
                               classifica=classifica)

    return render_template("inserisci.html", giocatori=list(classifica.keys()))

@app.route("/classifica")
def classifica():
    classifica = carica_classifica()
    return render_template("risultato.html",
                           giornata=None,
                           classifica=classifica)

if __name__ == "__main__":
    app.run(debug=True)
