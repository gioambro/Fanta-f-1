from flask import Flask, render_template, request, redirect, url_for
from punteggi import calcola_punteggio

app = Flask(__name__)

# Dizionario per salvare punteggi cumulativi
punteggi_totali = {f"Giocatore {i}": 0 for i in range(1, 7)}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        risultati_giornata = {}
        for i in range(1, 7):  # 6 giocatori
            dati = {
                "posizione": request.form.get(f"g{i}_pos"),
                "pole": request.form.get(f"g{i}_pole"),
                "fastest_lap": request.form.get(f"g{i}_fastest_lap"),
                "driver_day": request.form.get(f"g{i}_driver_day"),
                "fastest_pit": request.form.get(f"g{i}_fastest_pit"),
                "last_rows_points": request.form.get(f"g{i}_last_rows_points"),
                "griglia": request.form.get(f"g{i}_griglia"),
                "squalifica": request.form.get(f"g{i}_squalifica"),
                "dnf": request.form.get(f"g{i}_dnf"),
                "pen_6": request.form.get(f"g{i}_pen_6"),
                "pen_5": request.form.get(f"g{i}_pen_5"),
                "last_place": request.form.get(f"g{i}_last_place"),
                "no_q1": request.form.get(f"g{i}_no_q1"),
            }

            punteggio = calcola_punteggio(dati)
            risultati_giornata[f"Giocatore {i}"] = punteggio

            # aggiorna la classifica generale
            punteggi_totali[f"Giocatore {i}"] += punteggio

        return render_template(
            "risultato.html",
            giornata=risultati_giornata,
            classifica_generale=punteggi_totali
        )
    return render_template("inserisci.html")

if __name__ == "__main__":
    app.run(debug=True)
