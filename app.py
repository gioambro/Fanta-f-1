from flask import Flask, render_template, request
from punteggi import calcola_punteggio
import json, os, itertools

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

def calcola_classifica_generale(storico):
    totale_generale = {f"Giocatore {i}": 0 for i in range(1,7)}
    for giornata in storico:
        for g in range(1,7):
            totale_generale[f"Giocatore {g}"] += giornata.get(f"Giocatore {g}", 0)
    return sorted(totale_generale.items(), key=lambda x: x[1], reverse=True)

# Genera le coppie 1vs1 (per ora sequenziali, es: G1 vs G2, G3 vs G4, G5 vs G6)
def genera_scontri(giornata):
    giocatori = [f"Giocatore {i}" for i in range(1,7)]
    # Rotazione per avere scontri diversi nelle giornate
    rotazione = giocatori[1:]
    rotazione = rotazione[giornata % len(rotazione):] + rotazione[:giornata % len(rotazione)]
    abbinati = [giocatori[0]] + rotazione
    scontri = [(abbinati[i], abbinati[i+1]) for i in range(0, 6, 2)]
    return scontri

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        risultati = []
        giornata = len(carica_storico()) + 1
        punteggi_giornata = {"giornata": giornata}

        for i in range(1, 7):  # 6 giocatori
            totale_giocatore = 0
            ha_inserito = False

            for p in range(1, 3):  # 2 piloti
                dati = {
                    "pos": request.form.get(f"g{i}_p{p}_pos"),
                    "pole": request.form.get(f"g{i}_p{p}_pole"),
                    "fastest_lap": request.form.get(f"g{i}_p{p}_fastest_lap"),
                    "driver_day": request.form.get(f"g{i}_p{p}_driver_day"),
                    "fastest_pit": request.form.get(f"g{i}_p{p}_fastest_pit"),
                    "back_to_points": request.form.get(f"g{i}_p{p}_back_to_points"),
                    "pos_gain": request.form.get(f"g{i}_p{p}_pos_gain", 0),
                    "win": request.form.get(f"g{i}_p{p}_win"),
                    "podium": request.form.get(f"g{i}_p{p}_podium"),
                    "dsq": request.form.get(f"g{i}_p{p}_dsq"),
                    "dnf": request.form.get(f"g{i}_p{p}_dnf"),
                    "pen_6": request.form.get(f"g{i}_p{p}_pen_6"),
                    "pen_5": request.form.get(f"g{i}_p{p}_pen_5"),
                    "last": request.form.get(f"g{i}_p{p}_last"),
                    "q1": request.form.get(f"g{i}_p{p}_q1"),
                    "pos_lost": request.form.get(f"g{i}_p{p}_pos_lost", 0),
                }

                if any(dati.values()):
                    ha_inserito = True
                    totale_giocatore += calcola_punteggio(dati)

            if not ha_inserito:
                totale_giocatore = 0

            risultati.append((f"Giocatore {i}", totale_giocatore))
            punteggi_giornata[f"Giocatore {i}"] = totale_giocatore

        # Salva nello storico
        storico = carica_storico()
        storico.append(punteggi_giornata)
        salva_storico(storico)

        # Calcola classifica generale
        classifica_generale = calcola_classifica_generale(storico)

        # Genera scontri per la giornata
        scontri = genera_scontri(giornata)

        return render_template("risultato.html", 
                               risultati=risultati, 
                               giornata=giornata,
                               classifica_generale=classifica_generale,
                               scontri=scontri)

    return render_template("index.html")

@app.route("/classifica")
def classifica():
    storico = carica_storico()
    classifica_generale = calcola_classifica_generale(storico)
    return render_template("classifica.html", classifica_generale=classifica_generale)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
