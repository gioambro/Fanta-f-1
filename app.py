from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/calcola", methods=["POST"])
def calcola():
    risultato = {
        "posizione": int(request.form["posizione"]),
        "sprint": "sprint" in request.form,
        "pole": "pole" in request.form,
        "dnf": "dnf" in request.form
    }
    punti = calcola_punteggio(risultato)
    return render_template("risultato.html", punti=punti)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
