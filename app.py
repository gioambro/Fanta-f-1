import json
import os
from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)
STORICO_FILE = "storico.json"

def carica_storico():
    if os.path.exists(STORICO_FILE):
        with open(STORICO_FILE, "r") as f:
            return json.load(f)
    return []

def salva_storico(storico):
    with open(STORICO_FILE, "w") as f:
        json.dump(storico, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        risultati = []
        giornata = len(carica_storico()) + 1
        punteggi_giornata = {"giornata": giornata}

        for i in range(1, 7):  # 6 giocatori
            dati = {
                "pos": request.form.get(f"g{i}_pos"),
                "pole": request.form.get(f"g{i}_pole"),
                "fastest_lap": request.form.get(f"g{i}_fastest_lap"),
                "driver_day": request.form.get(f"g{i}_driver_day"),
                "fastest_pit": request.form.get(f"g{i}_fastest_pit"),
                "back_to_points": request.form.get(f"g{i}_back_to_points"),
                "pos_gain": request.form.get(f"g{i}_pos_gain", 0),
                "win": request.form.get(f"g{i}_win"),
                "podium": request.form.get(f"g{i}_podium"),
                "dsq": request.form.get(f"g{i}_dsq"),
                "dnf": request.form.get(f"g{i}_dnf"),
                "pen_6": request.form.get(f"g{i}_pen_6"),
                "pen_5": request.form.get(f"g{i}_pen_5"),
                "last": request.form.get(f"g{i}_last"),
                "q1": request.form.get(f"g{i}_q1"),
                "pos_lost": request.form.get(f"g{i}_pos_lost", 0),
            }
            punteggio = calcola_punteggio(dati)
            risultati.append((f"Giocatore {i}", punteggio))
            punteggi_giornata[f"Giocatore {i}"] = punteggio

        # Salva nello storico
        storico = carica_storico()
        storico.append(punteggi_giornata)
        salva_storico(storico)

        return render_template("risultato.html", risultati=risultati, giornata=giornata)

    return render_template("index.html")
