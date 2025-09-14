from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File di salvataggio
FILE_NOMI = "nomi_giocatori.json"
FILE_STORICO = "storico.json"

# Dati iniziali
NOMI_DEFAULT = [
    "Alfarumeno",
    "Stalloni",
    "WC in Geriatria",
    "Strolling Around",
    "Spartaboyz",
    "Vodkaredbull"
]

CLASSIFICA_DEFAULT = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# Funzione per caricare JSON
def carica_dati(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    else:
        with open(file, "w") as f:
            json.dump(default, f)
        return default

# Carico dati all'avvio
nomi_giocatori = carica_dati(FILE_NOMI, NOMI_DEFAULT)
classifica_generale = carica_dati(FILE_STORICO, CLASSIFICA_DEFAULT)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        # Qui puoi mettere la logica per calcolare i punteggi della giornata
        # Per ora aggiorniamo solo la classifica con valori di esempio
        for nome in nomi_giocatori:
            classifica_generale[nome] += 0  # <--- qui va inserito il punteggio calcolato

        # Salvo aggiornamenti
        with open(FILE_STORICO, "w") as f:
            json.dump(classifica_generale, f)

        return redirect(url_for("risultati"))

    return render_template("inserisci.html", nomi=nomi_giocatori)

@app.route("/risultati")
def risultati():
    return render_template("risultato.html",
                           classifica_generale=classifica_generale)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
