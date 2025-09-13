from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

STORICO_FILE = "storico.json"

# --- Funzione di calcolo punteggio ---
def calcola_punteggio(dati):
    punti = 0

    pos = dati.get("pos")
    griglia = dati.get("griglia")
    sprint = dati.get("sprint", False)

    # punti classifica ufficiale F1 (solo i primi 10)
    punti_classifica = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    if pos and pos <= len(punti_classifica):
        punti += punti_classifica[pos-1]

    # Sprint: punteggi diversi (solo top 8)
    if sprint and pos and pos <= 8:
        punti += [8, 7, 6, 5, 4, 3, 2, 1][pos-1]

    # BONUS
    if dati.get("pole"): punti += 2
    if dati.get("fastest_lap"): punti += 1
    if dati.get("driver_day"): punti += 1
    if dati.get("fastest_pit"): punti += 2
    if dati.get("last_rows_points"): punti += 2
    if dati.get("pos_gain"): punti += 0.5 * dati.get("pos_gain")

    # Vittoria e podio (non valgono nelle sprint)
    if not sprint:
        if dati.get("win"): punti += 3
        if dati.get("podium"): punti += 2

    # MALUS
    if dati.get("dsq"): punti -= 5
    if dati.get("dnf"): punti -= 3
    if dati.get("pen_6"): punti -= 4
    if dati.get("pen_5"): punti -= 3
    if dati.get("last_place"): punti -= 2
    if dati.get("no_q1"): punti -= 1
    if dati.get("pos_loss"): punti -= 0.5 * dati.get("pos_loss")

    return punti

# --- Home ---
@app.route("/")
def home():
    return render_template("home.html")

# --- Inserimento risultati ---
@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        giornata = []

        for g in range(1, 7):  # 6 giocatori
            totale = 0
            for p in range(1, 3):  # 2 piloti ciascuno
                prefix = f"g{g}_p{p}_"

                try:
                    pos = int(request.form.get(prefix + "pos") or 0)
                except:
                    pos = None

                try:
                    griglia = int(request.form.get(prefix + "griglia") or 0)
                except:
                    griglia = None

                dati = {
                    "pos": pos,
                    "griglia": griglia,
                    "sprint": request.form.get(prefix + "sprint") == "on",
                    "pole": request.form.get(prefix + "pole") == "on",
                    "fastest_lap": request.form.get(prefix + "fastest_lap") == "on",
                    "driver_day": request.form.get(prefix + "driver_day") == "on",
                    "fastest_pit": request.form.get(prefix + "fastest_pit") == "on",
                    "last_rows_points": request.form.get(prefix + "last_rows_points") == "on",
                    "win": request.form.get(prefix + "win") == "on",
                    "podium": request.form.get(prefix + "podium") == "on",
                    "dsq": request.form.get(prefix + "dsq") == "on",
                    "dnf": request.form.get(prefix + "dnf") == "on",
                    "pen_6": request.form.get(prefix + "pen_6") == "on",
                    "pen_5": request.form.get(prefix + "pen_5") == "on",
                    "last_place": request.form.get(prefix + "last_place") == "on",
                    "no_q1": request.form.get(prefix + "no_q1") == "on",
                }

                # calcolo posizioni guadagnate/perse
                if pos and griglia:
                    if pos < griglia:
                        dati["pos_gain"] = griglia - pos
                        dati["pos_loss"] = 0
                    elif pos > griglia:
                        dati["pos_gain"] = 0
                        dati["pos_loss"] = pos - griglia
                    else:
                        dati["pos_gain"] = 0
                        dati["pos_loss"] = 0
                else:
                    dati["pos_gain"] = 0
                    dati["pos_loss"] = 0

                totale += calcola_punteggio(dati)

            giornata.append({"giocatore": g, "punti": totale})

        # salva nello storico
        if os.path.exists(STORICO_FILE):
            with open(STORICO_FILE, "r") as f:
                storico = json.load(f)
        else:
            storico = []

        storico.append(giornata)

        with open(STORICO_FILE, "w") as f:
            json.dump(storico, f)

        return render_template("risultato.html", giornata=giornata, storico=storico)

    return render_template("inserisci.html")

if __name__ == "__main__":
    app.run(debug=True)
