from flask import Flask, request, jsonify

app = Flask(__name__)

# Punteggi base (senza malus della gomma bucata)
base_points = [6, 4, 3, 2, 1, 0]

@app.route("/calcola", methods=["POST"])
def calcola():
    dati = request.json
    pos = dati.get("posizione")
    if pos is None:
        return jsonify({"errore": "Devi specificare la posizione"}), 400

    # Calcolo punti (senza il malus della gomma bucata)
    punti = base_points[pos - 1]
    return jsonify({"punti": punti})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
