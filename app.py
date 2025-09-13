from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)

def leggi_pilota(form, prefix):
    return {
        "posizione": int(form.get(f"{prefix}_posizione", 20)),
        "sprint": f"{prefix}_sprint" in form,
        "pole": f"{prefix}_pole" in form,
        "fastest_lap": f"{prefix}_fastest_lap" in form,
        "driver_of_the_day": f"{prefix}_driver" in form,
        "fastest_pitstop": f"{prefix}_pitstop" in form,
        "posizioni_guadagnate": int(form.get(f"{prefix}_gain", 0)),
        "posizioni_perse": int(form.get(f"{prefix}_loss", 0)),
        "dnf": f"{prefix}_dnf" in form,
        "squalifica": f"{prefix}_squal" in form,
        "penalita_grave": f"{prefix}_pen_grave" in form,
        "penalita_leggera": f"{prefix}_pen_leggera" in form,
        "ultimo": f"{prefix}_last" in form,
        "vittoria": f"{prefix}_win" in form,
        "podio": f"{prefix}_podio" in form
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcola", methods=["POST"])
def calcola():
    punteggi_giocatori = []

    for g in range(1, 7):
        pilota1 = leggi_pilota(request.form, f"g{g}_p1")
        pilota2 = leggi_pilota(request.form, f"g{g}_p2")

        punti = calcola_punteggio(pilota1) + calcola_punteggio(pilota2)
        punteggi_giocatori.append({"giocatore": g, "punti": punti})

    return render_template("risultato.html", risultati=punteggi_giocatori)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
