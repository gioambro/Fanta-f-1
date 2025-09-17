from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dizionario per memorizzare i punteggi (per ora in memoria)
classifica = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        giocatore = request.form["giocatore"]
        punti = int(request.form["punti"])

        # Aggiorna la classifica
        if giocatore in classifica:
            classifica[giocatore] += punti
        else:
            classifica[giocatore] = punti

        return redirect(url_for("classifica_generale"))

    return render_template("inserisci.html")

@app.route("/classifica")
def classifica_generale():
    # Ordina la classifica per punti
    classifica_ordinata = sorted(classifica.items(), key=lambda x: x[1], reverse=True)
    return render_template("classifica.html", classifica_generale=classifica_ordinata)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
