from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        risultati = []
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

        return render_template("risultato.html", risultati=risultati)

    return render_template("index.html")


@app.route("/risultato")
def risultato():
    return render_template("risultato.html", risultati=[])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
