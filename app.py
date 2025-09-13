from flask import Flask, render_template, request
from punteggi import calcola_punteggio
import json, os

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
            totale_giocatore = 0
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
                totale_giocatore += calcola_punteggio(dati)

            risultati.append((f"Giocatore {i}", totale_giocatore))
            punteggi_giornata[f"Giocatore {i}"] = totale_giocatore

        # Salva nello storico
        storico = carica_storico()
        storico.append(punteggi_giornata)
        salva_storico(storico)

        return render_template("risultato.html", risultati=risultati, giornata=giornata)

    return render_template("index.html")

@app.route("/risultato")
def risultato():
    return render_template("risultato.html", risultati=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
