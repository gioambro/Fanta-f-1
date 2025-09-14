from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Giocatori e punteggi iniziali dopo 16 gare
giocatori = ["Alfarumeno", "Stalloni", "WC in Geriatria", "Strolling Around", "Spartaboyz", "Vodkaredbull"]
classifica_generale = {
    "Alfarumeno": 12,
    "Stalloni": 10,
    "WC in Geriatria": 10,
    "Strolling Around": 5,
    "Spartaboyz": 5,
    "Vodkaredbull": 2
}

# Variabile per le giornate
giornata_n = 17  # parte da 17 perché ci sono già state 16 gare

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inserisci', methods=['GET', 'POST'])
def inserisci():
    global giornata_n, classifica_generale

    if request.method == 'POST':
        classifica_giornata = {}
        for giocatore in giocatori:
            punti = request.form.get(f'punti_{giocatore}', 0)
            try:
                punti = float(punti)
            except:
                punti = 0
            classifica_giornata[giocatore] = punti
            classifica_generale[giocatore] += punti

        # Ordino la classifica generale per punteggio
        classifica_generale_ordinata = dict(
            sorted(classifica_generale.items(), key=lambda x: x[1], reverse=True)
        )

        giornata_corrente = giornata_n
        giornata_n += 1  # passo alla prossima gara

        return render_template(
            "risultato.html",
            giornata=giornata_corrente,
            classifica_giornata=classifica_giornata,
            classifica_generale=classifica_generale_ordinata
        )

    return render_template('inserisci.html', giocatori=giocatori)

if __name__ == '__main__':
    app.run(debug=True)
