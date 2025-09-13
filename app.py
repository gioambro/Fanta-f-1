from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcola", methods=["POST"])
def calcola():
    risultato = {
        "posizione": int(request.form.get("posizione", 20)),
        "sprint": "sprint" in request.form,
        "pole": "pole" in request.form,
        "fastest_lap": "fastest_lap" in request.form,
        "driver_of_the_day": "driver_of_the_day" in request.form,
        "fastest_pitstop": "fastest_pitstop" in request.form,
        "posizioni_guadagnate": int(request.form.get("posizioni_guadagnate", 0)),
        "posizioni_perse": int(request.form.get("posizioni_perse", 0)),
        "dnf": "dnf" in request.form,
        "squalifica": "squalifica" in request.form,
        "penalita_grave": "penalita_grave" in request.form,
        "penalita_leggera": "penalita_leggera" in request.form,
        "ultimo": "ultimo" in request.form,
        "vittoria": "vittoria" in request.form,
        "podio": "podio" in request.form
    }

    punti = calcola_punteggio(risultato)
    return render_template("risultato.html", punti=punti)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
