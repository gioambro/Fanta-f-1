from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcola', methods=['POST'])
def calcola():
    try:
        posizione = request.form.get("posizione")
        sprint = request.form.get("sprint")
        pole = request.form.get("pole")
        dnf = request.form.get("dnf")

        # Controllo che la posizione sia un numero valido
        if posizione and posizione.isdigit():
            posizione = int(posizione)
        else:
            posizione = None

        # Punti base in base alla posizione
        base_points = {
            1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
            6: 8, 7: 6, 8: 4, 9: 2, 10: 1
        }

        punti = 0
        if posizione in base_points:
            punti += base_points[posizione]

        # Sprint race
        if sprint:
            punti += 3

        # Pole position
        if pole:
            punti += 2

        # DNF (non finisce la gara)
        if dnf:
            punti = 0

        return render_template("risultato.html", punti=punti)

    except Exception as e:
        return f"Errore nel calcolo: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
