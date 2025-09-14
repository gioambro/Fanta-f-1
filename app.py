from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Classifica iniziale con i punteggi dopo 16 gare
classifica_generale = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inserisci", methods=["GET", "POST"])
def inserisci():
    if request.method == "POST":
        # Aggiorna i punteggi con quelli inseriti
        for giocatore in classifica_generale.keys():
            punti = request.form.get(giocatore)
            if punti and punti.isdigit():
                classifica_generale[giocatore] += int(punti)
        return redirect(url_for("risultati"))

    return render_template("inserisci.html", nomi=classifica_generale.keys())

@app.route("/risultati")
def risultati():
    # Ordina la classifica dal punteggio più alto al più basso
    classifica_ordinata = dict(
        sorted(classifica_generale.items(), key=lambda x: x[1], reverse=True)
    )
    return render_template("risultato.html", classifica_generale=classifica_ordinata)

if __name__ == "__main__":
    app.run(debug=True)
