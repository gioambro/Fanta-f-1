from flask import Flask, render_template, request
from punteggi import calcola_punteggio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcola', methods=['POST'])
def calcola():
    punteggi = {}
    for g in range(1, 7):  # 6 giocatori
        pos = request.form.get(f"g{g}_pos")
        sprint = request.form.get(f"g{g}_sprint")
        pole = request.form.get(f"g{g}_pole")
        dnf = request.form.get(f"g{g}_dnf")

        if pos:  # solo se inserita una posizione
            pos = int(pos)
            punti = calcola_punteggio(pos, sprint, pole, dnf)
            punteggi[f"Giocatore {g}"] = punti

    return render_template('risultato.html', punteggi=punteggi)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
